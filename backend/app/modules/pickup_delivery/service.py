import uuid
from datetime import UTC, date, datetime, timedelta

from sqlalchemy.orm import Session, joinedload

from app.core.exceptions import NotFoundException, ValidationException
from app.modules.customers.models import Customer
from app.modules.customers.schemas import normalize_phone_e164
from app.modules.orders.models import Order, OrderHandoff, OrderItem, OrderStatusHistory
from app.modules.orders.service import OrderService
from app.modules.pickup_delivery.models import (
    DeliveryStatusHistory,
    DeliveryTask,
    DeliveryTaskStatus,
    DeliveryTaskType,
    PickupRequest,
    PickupStatus,
)
from app.modules.pickup_delivery.schemas import (
    DeliveryTaskCreate,
    DeliveryTaskStatusUpdate,
    PickupConfirmPayload,
    PickupConvertToOrderPayload,
    PickupRejectPayload,
    PublicPickupRequestCreate,
)
from app.modules.services.models import Service
from app.modules.tracking.models import TrackingToken
from app.modules.tracking.service import TrackingService
from app.modules.users.models import User


class PickupDeliveryService:
    @classmethod
    def generate_pickup_number(cls, db: Session, business_id: uuid.UUID) -> str:
        """
        Generate atomic sequential pickup request number: PCK-YYYYMMDD-XXXX
        """
        today_str = datetime.now(UTC).strftime("%Y%m%d")
        prefix = f"PCK-{today_str}-"

        latest = (
            db.query(PickupRequest.request_number)
            .filter(
                PickupRequest.business_id == business_id,
                PickupRequest.request_number.like(f"{prefix}%"),
            )
            .order_by(PickupRequest.request_number.desc())
            .first()
        )

        if latest:
            seq_num = int(latest[0].split("-")[-1]) + 1
        else:
            seq_num = 1

        return f"{prefix}{seq_num:04d}"

    @classmethod
    def create_public_pickup_request(
        cls,
        db: Session,
        business_id: uuid.UUID,
        payload: PublicPickupRequestCreate,
    ) -> tuple[PickupRequest, str]:
        """
        Handle customer pickup intake.
        Links customer if phone exists or creates record, generates sequential request number,
        and generates cryptographically secure tracking token.
        """
        phone_e164 = normalize_phone_e164(payload.phone_e164)

        # Check existing customer
        customer = (
            db.query(Customer)
            .filter(
                Customer.business_id == business_id,
                Customer.phone_e164 == phone_e164,
            )
            .first()
        )
        if not customer:
            customer = Customer(
                business_id=business_id,
                full_name=payload.requester_name.strip(),
                phone_e164=phone_e164,
                address=payload.pickup_address.strip(),
                is_active=True,
            )
            db.add(customer)
            db.flush()

        req_number = cls.generate_pickup_number(db, business_id)

        pickup = PickupRequest(
            business_id=business_id,
            customer_id=customer.id,
            request_number=req_number,
            requester_name=payload.requester_name.strip(),
            phone_e164=phone_e164,
            pickup_address=payload.pickup_address.strip(),
            requested_date=payload.requested_date,
            requested_time_start=payload.requested_time_start,
            requested_time_end=payload.requested_time_end,
            status=PickupStatus.REQUESTED.value,
            notes=payload.notes.strip() if payload.notes else None,
        )
        db.add(pickup)
        db.flush()

        # Generate tracking token for pickup
        raw_token, token_hash = TrackingService.generate_token_pair()
        tracking_token = TrackingToken(
            order_id=None,
            pickup_request_id=pickup.id,
            token_hash=token_hash,
            expires_at=datetime.now(UTC) + timedelta(days=90),
            created_by=None,
        )
        db.add(tracking_token)
        db.commit()
        db.refresh(pickup)

        return pickup, raw_token

    @classmethod
    def list_pickup_requests(
        cls,
        db: Session,
        business_id: uuid.UUID,
        status_filter: str | None = None,
        date_filter: date | None = None,
    ) -> list[PickupRequest]:
        query = (
            db.query(PickupRequest)
            .filter(PickupRequest.business_id == business_id)
            .order_by(PickupRequest.created_at.desc())
        )
        if status_filter:
            query = query.filter(PickupRequest.status == status_filter)
        if date_filter:
            query = query.filter(PickupRequest.requested_date == date_filter)
        return query.all()

    @classmethod
    def get_pickup_request(
        cls,
        db: Session,
        pickup_id: uuid.UUID,
        business_id: uuid.UUID,
    ) -> PickupRequest:
        pickup = (
            db.query(PickupRequest)
            .filter(
                PickupRequest.id == pickup_id,
                PickupRequest.business_id == business_id,
            )
            .first()
        )
        if not pickup:
            raise NotFoundException("Permintaan penjemputan tidak ditemukan.")
        return pickup

    @classmethod
    def confirm_pickup_request(
        cls,
        db: Session,
        pickup_id: uuid.UUID,
        business_id: uuid.UUID,
        payload: PickupConfirmPayload,
        staff_id: uuid.UUID,
    ) -> PickupRequest:
        pickup = cls.get_pickup_request(db, pickup_id, business_id)

        if pickup.status not in (PickupStatus.REQUESTED.value, PickupStatus.CONFIRMED.value):
            raise ValidationException(
                f"Permintaan penjemputan dengan status '{pickup.status}' tidak dapat dikonfirmasi."
            )

        pickup.confirmed_start_at = payload.confirmed_start_at
        pickup.confirmed_end_at = payload.confirmed_end_at
        if payload.notes:
            pickup.notes = payload.notes

        # If courier assigned, dispatch a DeliveryTask (PICKUP)
        if payload.courier_user_id:
            courier = (
                db.query(User)
                .filter(
                    User.id == payload.courier_user_id,
                    User.business_id == business_id,
                    User.is_active.is_(True),
                )
                .first()
            )
            if not courier:
                raise ValidationException("Kurir yang dipilih tidak aktif atau tidak ditemukan.")

            pickup.status = PickupStatus.ASSIGNED.value

            # Create or update task
            task = (
                db.query(DeliveryTask)
                .filter(DeliveryTask.pickup_request_id == pickup.id)
                .first()
            )
            if not task:
                task = DeliveryTask(
                    business_id=business_id,
                    task_type=DeliveryTaskType.PICKUP.value,
                    pickup_request_id=pickup.id,
                    order_id=None,
                    courier_user_id=courier.id,
                    scheduled_start_at=payload.confirmed_start_at,
                    scheduled_end_at=payload.confirmed_end_at,
                    status=DeliveryTaskStatus.ASSIGNED.value,
                    recipient_name=pickup.requester_name,
                    destination_address=pickup.pickup_address,
                    destination_phone=pickup.phone_e164,
                    created_by=staff_id,
                )
                db.add(task)
                db.flush()

                history = DeliveryStatusHistory(
                    delivery_task_id=task.id,
                    from_status=None,
                    to_status=DeliveryTaskStatus.ASSIGNED.value,
                    changed_by=staff_id,
                    reason="Penugasan kurir jemput cucian",
                )
                db.add(history)
            else:
                task.courier_user_id = courier.id
                task.status = DeliveryTaskStatus.ASSIGNED.value
        else:
            pickup.status = PickupStatus.CONFIRMED.value

        db.commit()
        db.refresh(pickup)
        return pickup

    @classmethod
    def reject_pickup_request(
        cls,
        db: Session,
        pickup_id: uuid.UUID,
        business_id: uuid.UUID,
        payload: PickupRejectPayload,
    ) -> PickupRequest:
        pickup = cls.get_pickup_request(db, pickup_id, business_id)

        if pickup.status in (PickupStatus.CONVERTED.value, PickupStatus.AT_LAUNDRY.value, PickupStatus.REJECTED.value):
            raise ValidationException(
                f"Permintaan penjemputan berstatus '{pickup.status}' tidak dapat ditolak."
            )

        pickup.status = PickupStatus.REJECTED.value
        pickup.rejection_reason = payload.rejection_reason.strip()

        # Cancel any active tasks
        tasks = db.query(DeliveryTask).filter(DeliveryTask.pickup_request_id == pickup.id).all()
        for t in tasks:
            t.status = DeliveryTaskStatus.CANCELLED.value

        db.commit()
        db.refresh(pickup)
        return pickup

    @classmethod
    def convert_pickup_to_order(
        cls,
        db: Session,
        pickup_id: uuid.UUID,
        business_id: uuid.UUID,
        payload: PickupConvertToOrderPayload,
        staff_id: uuid.UUID,
    ) -> Order:
        """
        Atomic conversion of a completed pickup into an official laundry Order (DEC-10).
        Ensures exactly 1 order per pickup request and enforces 'AT_LAUNDRY' or 'PICKED_UP'.
        """
        pickup = cls.get_pickup_request(db, pickup_id, business_id)

        if pickup.status == PickupStatus.CONVERTED.value:
            raise ValidationException("Permintaan penjemputan ini sudah pernah dikonversi menjadi nota pesanan.")

        if pickup.status not in (PickupStatus.PICKED_UP.value, PickupStatus.AT_LAUNDRY.value, PickupStatus.ASSIGNED.value, PickupStatus.CONFIRMED.value):
            raise ValidationException(
                f"Permintaan berstatus '{pickup.status}' belum siap dikonversi. Cucian harus sudah diterima/diantar."
            )

        # Ensure Customer
        customer = pickup.customer
        if not customer:
            customer = (
                db.query(Customer)
                .filter(Customer.business_id == business_id, Customer.phone_e164 == pickup.phone_e164)
                .first()
            )
            if not customer:
                customer = Customer(
                    business_id=business_id,
                    full_name=pickup.requester_name,
                    phone_e164=pickup.phone_e164,
                    address=pickup.pickup_address,
                    is_active=True,
                )
                db.add(customer)
                db.flush()
            pickup.customer_id = customer.id

        # Verify Service
        service = (
            db.query(Service)
            .filter(Service.id == payload.service_id, Service.business_id == business_id)
            .first()
        )
        if not service or not service.is_active:
            raise ValidationException("Layanan laundry yang dipilih tidak ditemukan atau tidak aktif.")

        # Pricing engine calculation
        from app.modules.orders.domain.pricing import PricingEngine
        pricing_inputs = [(service.pricing_type, payload.quantity, service.unit_price)]
        price_result = PricingEngine.calculate_order(
            items=pricing_inputs,
            extra_charge_amount=payload.extra_charge_amount,
            delivery_fee_amount=payload.delivery_fee_amount,
        )

        order_number = OrderService.generate_order_number(db, business_id)
        now = datetime.now(UTC)
        est_completion = now + timedelta(hours=service.estimated_hours or 24)

        order = Order(
            business_id=business_id,
            order_number=order_number,
            customer_id=customer.id,
            pickup_request_id=pickup.id,
            created_by=staff_id,
            operational_status="RECEIVED",
            intake_method="COURIER_PICKUP",
            return_method=payload.return_method,
            subtotal_amount=price_result.subtotal_amount,
            extra_charge_amount=price_result.extra_charge_amount,
            delivery_fee_amount=price_result.delivery_fee_amount,
            total_amount=price_result.total_amount,
            estimated_completion_at=est_completion,
            customer_notes=payload.customer_notes.strip() if payload.customer_notes else pickup.notes,
            internal_notes=payload.internal_notes.strip() if payload.internal_notes else f"Dikonversi dari jemputan {pickup.request_number}",
            version=1,
        )
        db.add(order)
        db.flush()

        # Add Order Item
        line_res = price_result.line_results[0]
        order_item = OrderItem(
            order_id=order.id,
            service_id=service.id,
            service_name_snapshot=service.name,
            pricing_type_snapshot=service.pricing_type,
            unit_snapshot=service.unit,
            quantity=line_res.measured_quantity,
            unit_price_snapshot=service.unit_price,
            line_total_amount=line_res.line_total,
            requires_ironing_snapshot=service.requires_ironing,
        )
        db.add(order_item)

        # Status History
        history = OrderStatusHistory(
            order_id=order.id,
            from_status=None,
            to_status="RECEIVED",
            changed_by=staff_id,
            reason=f"Pesanan dibuat dari penjemputan {pickup.request_number}",
        )
        db.add(history)

        # Generate order tracking token
        _, token_hash = TrackingService.generate_token_pair()
        trk_order = TrackingToken(
            order_id=order.id,
            pickup_request_id=None,
            token_hash=token_hash,
            expires_at=now + timedelta(days=90),
            created_by=staff_id,
        )
        db.add(trk_order)

        # Update pickup request state to CONVERTED
        pickup.status = PickupStatus.CONVERTED.value

        db.commit()
        db.refresh(order)
        return order

    # -------------------------------------------------------------
    # Delivery Tasks (Courier Dispatch)
    # -------------------------------------------------------------
    @classmethod
    def create_delivery_task(
        cls,
        db: Session,
        business_id: uuid.UUID,
        payload: DeliveryTaskCreate,
        creator_id: uuid.UUID,
    ) -> DeliveryTask:
        if payload.task_type == DeliveryTaskType.PICKUP.value:
            if not payload.pickup_request_id:
                raise ValidationException("Tugas PICKUP wajib mencantumkan pickup_request_id.")
            if payload.order_id:
                raise ValidationException("Tugas PICKUP tidak boleh mencantumkan order_id.")
        elif payload.task_type == DeliveryTaskType.DELIVERY.value:
            if not payload.order_id:
                raise ValidationException("Tugas DELIVERY wajib mencantumkan order_id.")
            if payload.pickup_request_id:
                raise ValidationException("Tugas DELIVERY tidak boleh mencantumkan pickup_request_id.")
        else:
            raise ValidationException(f"Tipe tugas '{payload.task_type}' tidak valid.")

        task_status = (
            DeliveryTaskStatus.ASSIGNED.value
            if payload.courier_user_id
            else DeliveryTaskStatus.PENDING.value
        )

        task = DeliveryTask(
            business_id=business_id,
            task_type=payload.task_type,
            pickup_request_id=payload.pickup_request_id,
            order_id=payload.order_id,
            courier_user_id=payload.courier_user_id,
            scheduled_start_at=payload.scheduled_start_at,
            scheduled_end_at=payload.scheduled_end_at,
            status=task_status,
            recipient_name=payload.recipient_name,
            destination_address=payload.destination_address.strip(),
            destination_phone=payload.destination_phone.strip() if payload.destination_phone else None,
            created_by=creator_id,
        )
        db.add(task)
        db.flush()

        history = DeliveryStatusHistory(
            delivery_task_id=task.id,
            from_status=None,
            to_status=task_status,
            changed_by=creator_id,
            reason="Tugas kurir dibuat",
        )
        db.add(history)

        db.commit()
        db.refresh(task)
        return task

    @classmethod
    def list_delivery_tasks(
        cls,
        db: Session,
        business_id: uuid.UUID,
        courier_user_id: uuid.UUID | None = None,
        status_filter: str | None = None,
    ) -> list[DeliveryTask]:
        query = (
            db.query(DeliveryTask)
            .options(
                joinedload(DeliveryTask.courier),
                joinedload(DeliveryTask.order),
                joinedload(DeliveryTask.status_history),
            )
            .filter(DeliveryTask.business_id == business_id)
            .order_by(DeliveryTask.created_at.desc())
        )
        if courier_user_id:
            query = query.filter(DeliveryTask.courier_user_id == courier_user_id)
        if status_filter:
            query = query.filter(DeliveryTask.status == status_filter)
        return query.all()

    @classmethod
    def get_delivery_task(
        cls,
        db: Session,
        task_id: uuid.UUID,
        business_id: uuid.UUID,
    ) -> DeliveryTask:
        task = (
            db.query(DeliveryTask)
            .options(
                joinedload(DeliveryTask.courier),
                joinedload(DeliveryTask.order),
                joinedload(DeliveryTask.status_history).joinedload(DeliveryStatusHistory.user),
            )
            .filter(
                DeliveryTask.id == task_id,
                DeliveryTask.business_id == business_id,
            )
            .first()
        )
        if not task:
            raise NotFoundException("Tugas antar-jemput tidak ditemukan.")
        return task

    @classmethod
    def update_delivery_task_status(
        cls,
        db: Session,
        task_id: uuid.UUID,
        business_id: uuid.UUID,
        payload: DeliveryTaskStatusUpdate,
        user_id: uuid.UUID,
    ) -> DeliveryTask:
        task = cls.get_delivery_task(db, task_id, business_id)

        # Invariants: Terminal states immutable
        if task.status in (DeliveryTaskStatus.COMPLETED.value, DeliveryTaskStatus.CANCELLED.value):
            raise ValidationException(f"Tugas yang sudah '{task.status}' tidak dapat diubah lagi.")

        if payload.to_status == DeliveryTaskStatus.FAILED.value and not payload.failure_reason:
            raise ValidationException("Status GAGAL memerlukan alasan kegagalan.")

        prev_status = task.status
        task.status = payload.to_status

        if payload.failure_reason:
            task.failure_reason = payload.failure_reason.strip()
        if payload.proof_photo_path:
            task.proof_photo_path = payload.proof_photo_path.strip()

        now = datetime.now(UTC)

        # Completion handling
        if payload.to_status == DeliveryTaskStatus.COMPLETED.value:
            task.completed_at = now

            # If task is PICKUP, coordinate with pickup_requests
            if task.task_type == DeliveryTaskType.PICKUP.value and task.pickup_request_id:
                pickup = (
                    db.query(PickupRequest)
                    .filter(PickupRequest.id == task.pickup_request_id)
                    .first()
                )
                if pickup:
                    pickup.status = PickupStatus.AT_LAUNDRY.value

            # If task is DELIVERY and linked to order, coordinate with order_handoffs
            if task.task_type == DeliveryTaskType.DELIVERY.value and task.order_id:
                order = db.query(Order).filter(Order.id == task.order_id).first()
                if order:
                    handoff = (
                        db.query(OrderHandoff)
                        .filter(OrderHandoff.order_id == order.id)
                        .first()
                    )
                    if not handoff:
                        handoff = OrderHandoff(
                            order_id=order.id,
                            delivery_task_id=task.id,
                            handoff_method="COURIER_DELIVERY",
                            received_by_name=payload.received_by_name or task.recipient_name or "Pelanggan",
                            confirmed_by_user_id=user_id,
                            notes=payload.notes,
                        )
                        db.add(handoff)
                    else:
                        handoff.delivery_task_id = task.id
                        handoff.received_by_name = payload.received_by_name or handoff.received_by_name

                    # Move order status to COMPLETED
                    if order.operational_status == "READY":
                        order.operational_status = "COMPLETED"
                        order.version += 1
                        hist = OrderStatusHistory(
                            order_id=order.id,
                            from_status="READY",
                            to_status="COMPLETED",
                            changed_by=user_id,
                            reason="Pesanan selesai diantar oleh kurir ke pelanggan",
                        )
                        db.add(hist)

        # Record History
        history = DeliveryStatusHistory(
            delivery_task_id=task.id,
            from_status=prev_status,
            to_status=payload.to_status,
            changed_by=user_id,
            reason=payload.failure_reason or payload.notes or f"Perubahan status ke {payload.to_status}",
        )
        db.add(history)

        db.commit()
        db.refresh(task)
        return task

