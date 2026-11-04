import React, { useCallback, useEffect, useState } from 'react';
import { useAuth } from '../../context/use-auth';
import { apiClient, ApiError, type ApiResponse } from '../../lib/api-client';
import { pickupDeliveryApi } from '../../services/pickup-delivery';
import type {
  DeliveryTask,
  DeliveryTaskStatus,
  PickupRequest,
  PickupStatus,
} from '../../types/pickup-delivery';
import type { UserSummary } from '../../types/auth';
import type { LaundryService } from '../../types/services';
import {
  Truck,
  Package,
  CheckCircle2,
  AlertCircle,
  Phone,
  MapPin,
  User as UserIcon,
  X,
  Plus,
  Calendar,
  RefreshCw,
  ExternalLink,
  Navigation,
} from 'lucide-react';

export const DeliveryPage: React.FC = () => {
  const { user } = useAuth();
  const isCourier = user?.role === 'COURIER';
  const isCashierOrOwner = user?.role === 'OWNER' || user?.role === 'CASHIER';

  // Navigation tab for Cashier/Owner: 'pickups' | 'tasks'
  const [adminTab, setAdminTab] = useState<'pickups' | 'tasks'>('pickups');

  // Courier state
  const [courierTasks, setCourierTasks] = useState<DeliveryTask[]>([]);
  const [courierFilter, setCourierFilter] = useState<'ALL' | 'ACTIVE' | 'DONE'>('ACTIVE');

  // Admin state
  const [pickups, setPickups] = useState<PickupRequest[]>([]);
  const [pickupFilter, setPickupFilter] = useState<string>('');
  const [allTasks, setAllTasks] = useState<DeliveryTask[]>([]);
  const [taskFilter, setTaskFilter] = useState<string>('');

  // Aux state (Couriers and Services)
  const [couriers, setCouriers] = useState<UserSummary[]>([]);
  const [services, setServices] = useState<LaundryService[]>([]);

  // Common UI state
  const [isLoading, setIsLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);

  // Modals
  // 1. Confirm & Assign Pickup
  const [assignModal, setAssignModal] = useState<{ open: boolean; pickup: PickupRequest | null }>({
    open: false,
    pickup: null,
  });
  const [confirmStartAt, setConfirmStartAt] = useState('');
  const [confirmEndAt, setConfirmEndAt] = useState('');
  const [selectedCourierId, setSelectedCourierId] = useState('');
  const [assignNotes, setAssignNotes] = useState('');

  // 2. Reject Pickup
  const [rejectModal, setRejectModal] = useState<{ open: boolean; pickup: PickupRequest | null }>({
    open: false,
    pickup: null,
  });
  const [rejectReason, setRejectReason] = useState('');

  // 3. Convert Pickup to Order (DEC-10)
  const [convertModal, setConvertModal] = useState<{ open: boolean; pickup: PickupRequest | null }>({
    open: false,
    pickup: null,
  });
  const [convertServiceId, setConvertServiceId] = useState('');
  const [convertQuantity, setConvertQuantity] = useState('3.0');
  const [convertDeliveryFee, setConvertDeliveryFee] = useState('0');
  const [convertNotes, setConvertNotes] = useState('');
  const [convertReturnMethod, setConvertReturnMethod] = useState<'SELF_PICKUP' | 'HOME_DELIVERY'>('SELF_PICKUP');

  // 4. Complete Delivery Task (for courier)
  const [completeTaskModal, setCompleteTaskModal] = useState<{ open: boolean; task: DeliveryTask | null }>({
    open: false,
    task: null,
  });
  const [recipientName, setRecipientName] = useState('');
  const [completionNotes, setCompletionNotes] = useState('');

  // 5. Fail Task Modal
  const [failTaskModal, setFailTaskModal] = useState<{ open: boolean; task: DeliveryTask | null }>({
    open: false,
    task: null,
  });
  const [failureReason, setFailureReason] = useState('');

  // 6. Create Delivery Task Modal (Cashier)
  const [createTaskModal, setCreateTaskModal] = useState(false);
  const [newTaskRecipient, setNewTaskRecipient] = useState('');
  const [newTaskPhone, setNewTaskPhone] = useState('');
  const [newTaskAddress, setNewTaskAddress] = useState('');
  const [newTaskCourierId, setNewTaskCourierId] = useState('');

  const [isSubmitting, setIsSubmitting] = useState(false);

  // Fetch data
  const loadData = useCallback(async () => {
    setIsLoading(true);
    setErrorMsg(null);
    try {
      if (isCourier) {
        const myTasks = await pickupDeliveryApi.listMyTasks();
        setCourierTasks(myTasks);
      } else {
        const [pickupList, taskList, userList, serviceList] = await Promise.all([
          pickupDeliveryApi.listPickupRequests(),
          pickupDeliveryApi.listDeliveryTasks(),
          apiClient<ApiResponse<UserSummary[]>>('/users').catch(() => ({ data: [] })),
          apiClient<ApiResponse<LaundryService[]>>('/services').catch(() => ({ data: [] })),
        ]);
        setPickups(pickupList);
        setAllTasks(taskList);
        setCouriers(userList.data.filter((u) => u.role === 'COURIER' && u.is_active));
        setServices(serviceList.data.filter((s) => s.is_active));
        if (serviceList.data.length > 0 && !convertServiceId) {
          setConvertServiceId(serviceList.data[0].id);
        }
      }
    } catch (err) {
      if (err instanceof ApiError) {
        setErrorMsg(err.message);
      } else {
        setErrorMsg('Gagal memuat data logistik penjemputan & pengantaran.');
      }
    } finally {
      setIsLoading(false);
    }
  }, [isCourier, convertServiceId]);

  useEffect(() => {
    let ignore = false;
    async function fetchData() {
      try {
        if (isCourier) {
          const myTasks = await pickupDeliveryApi.listMyTasks();
          if (!ignore) setCourierTasks(myTasks);
        } else {
          const [pickupList, taskList, userList, serviceList] = await Promise.all([
            pickupDeliveryApi.listPickupRequests(),
            pickupDeliveryApi.listDeliveryTasks(),
            apiClient<ApiResponse<UserSummary[]>>('/users').catch(() => ({ data: [] })),
            apiClient<ApiResponse<LaundryService[]>>('/services').catch(() => ({ data: [] })),
          ]);
          if (!ignore) {
            setPickups(pickupList);
            setAllTasks(taskList);
            setCouriers(userList.data.filter((u) => u.role === 'COURIER' && u.is_active));
            setServices(serviceList.data.filter((s) => s.is_active));
            if (serviceList.data.length > 0 && !convertServiceId) {
              setConvertServiceId(serviceList.data[0].id);
            }
          }
        }
      } catch (err) {
        if (!ignore) {
          if (err instanceof ApiError) {
            setErrorMsg(err.message);
          } else {
            setErrorMsg('Gagal memuat data logistik penjemputan & pengantaran.');
          }
        }
      } finally {
        if (!ignore) {
          setIsLoading(false);
        }
      }
    }
    fetchData();
    return () => {
      ignore = true;
    };
  }, [isCourier, convertServiceId]);

  // Status Badge formatting
  const renderPickupBadge = (status: PickupStatus) => {
    switch (status) {
      case 'REQUESTED':
        return <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-amber-50 text-amber-800 border border-amber-200">Menunggu Konfirmasi</span>;
      case 'CONFIRMED':
        return <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-blue-50 text-blue-800 border border-blue-200">Terkonfirmasi</span>;
      case 'ASSIGNED':
        return <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-indigo-50 text-indigo-800 border border-indigo-200">Kurir Ditugaskan</span>;
      case 'PICKED_UP':
        return <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-800 border border-emerald-200">Sudah Dijemput</span>;
      case 'CONVERTED':
        return <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-teal-50 text-teal-800 border border-teal-200">Pesanan Dibuat</span>;
      case 'REJECTED':
      case 'CANCELLED':
        return <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-rose-50 text-rose-800 border border-rose-200">Dibatalkan</span>;
      default:
        return <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-slate-100 text-slate-700">{status}</span>;
    }
  };

  const renderTaskBadge = (status: DeliveryTaskStatus) => {
    switch (status) {
      case 'ASSIGNED':
        return <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-amber-50 text-amber-800 border border-amber-200">Ditugaskan</span>;
      case 'EN_ROUTE':
        return <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-blue-50 text-blue-800 border border-blue-200">Dalam Perjalanan</span>;
      case 'ARRIVED':
        return <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-indigo-50 text-indigo-800 border border-indigo-200">Tiba di Lokasi</span>;
      case 'COMPLETED':
        return <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-800 border border-emerald-200">Selesai</span>;
      case 'FAILED':
        return <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-rose-50 text-rose-800 border border-rose-200">Gagal</span>;
      case 'CANCELLED':
        return <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-slate-100 text-slate-700 border border-slate-200">Dibatalkan</span>;
      default:
        return <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-slate-100 text-slate-700">{status}</span>;
    }
  };

  // Courier Actions
  const handleUpdateTaskStatus = async (
    taskId: string,
    toStatus: DeliveryTaskStatus,
    extra?: { received_by_name?: string; failure_reason?: string; notes?: string }
  ) => {
    setIsSubmitting(true);
    setErrorMsg(null);
    try {
      await pickupDeliveryApi.updateTaskStatus(taskId, {
        to_status: toStatus,
        received_by_name: extra?.received_by_name,
        failure_reason: extra?.failure_reason,
        notes: extra?.notes,
      });
      setSuccessMsg(`Status tugas berhasil diubah ke: ${toStatus}`);
      await loadData();
    } catch (err) {
      if (err instanceof ApiError) {
        setErrorMsg(err.message);
      } else {
        setErrorMsg('Gagal memperbarui status tugas.');
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  // Cashier: Open Confirm Modal
  const openConfirmModal = (pickup: PickupRequest) => {
    const now = new Date();
    const startStr = new Date(now.getTime() + 60 * 60 * 1000).toISOString().slice(0, 16);
    const endStr = new Date(now.getTime() + 180 * 60 * 1000).toISOString().slice(0, 16);
    setConfirmStartAt(startStr);
    setConfirmEndAt(endStr);
    setSelectedCourierId(couriers.length > 0 ? couriers[0].id : '');
    setAssignNotes('');
    setAssignModal({ open: true, pickup });
  };

  // Cashier: Submit Confirm
  const handleSubmitConfirm = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!assignModal.pickup) return;
    setIsSubmitting(true);
    setErrorMsg(null);
    try {
      await pickupDeliveryApi.confirmPickupRequest(assignModal.pickup.id, {
        confirmed_start_at: new Date(confirmStartAt).toISOString(),
        confirmed_end_at: new Date(confirmEndAt).toISOString(),
        courier_user_id: selectedCourierId || undefined,
        notes: assignNotes || undefined,
      });
      setSuccessMsg('Penjemputan dikonfirmasi dan kurir berhasil ditugaskan.');
      setAssignModal({ open: false, pickup: null });
      await loadData();
    } catch (err) {
      if (err instanceof ApiError) {
        setErrorMsg(err.message);
      } else {
        setErrorMsg('Gagal mengonfirmasi penjemputan.');
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  // Cashier: Submit Reject
  const handleSubmitReject = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!rejectModal.pickup) return;
    setIsSubmitting(true);
    setErrorMsg(null);
    try {
      await pickupDeliveryApi.rejectPickupRequest(rejectModal.pickup.id, {
        rejection_reason: rejectReason,
      });
      setSuccessMsg('Permintaan penjemputan berhasil ditolak.');
      setRejectModal({ open: false, pickup: null });
      await loadData();
    } catch (err) {
      if (err instanceof ApiError) {
        setErrorMsg(err.message);
      } else {
        setErrorMsg('Gagal menolak permintaan penjemputan.');
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  // Cashier: Open Convert Modal
  const openConvertModal = (pickup: PickupRequest) => {
    setConvertModal({ open: true, pickup });
    setConvertQuantity('3.0');
    setConvertDeliveryFee('0');
    setConvertNotes(pickup.notes || '');
    setConvertReturnMethod('SELF_PICKUP');
  };

  // Cashier: Submit Convert to Order (DEC-10)
  const handleSubmitConvert = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!convertModal.pickup) return;
    setIsSubmitting(true);
    setErrorMsg(null);
    try {
      const res = await pickupDeliveryApi.convertToOrder(convertModal.pickup.id, {
        service_id: convertServiceId,
        quantity: parseFloat(convertQuantity),
        delivery_fee_amount: parseInt(convertDeliveryFee, 10) || 0,
        return_method: convertReturnMethod,
        customer_notes: convertNotes || undefined,
      });
      setSuccessMsg(`Pesanan resmi berhasil dibuat: ${res.order_number}!`);
      setConvertModal({ open: false, pickup: null });
      await loadData();
    } catch (err) {
      if (err instanceof ApiError) {
        setErrorMsg(err.message);
      } else {
        setErrorMsg('Gagal mengonversi penjemputan menjadi pesanan.');
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  // Cashier: Submit Create Delivery Task
  const handleCreateTask = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setErrorMsg(null);
    try {
      await pickupDeliveryApi.createDeliveryTask({
        task_type: 'DELIVERY',
        recipient_name: newTaskRecipient,
        destination_phone: newTaskPhone,
        destination_address: newTaskAddress,
        courier_user_id: newTaskCourierId || undefined,
      });
      setSuccessMsg('Tugas pengantaran baru berhasil dibuat.');
      setCreateTaskModal(false);
      setNewTaskRecipient('');
      setNewTaskPhone('');
      setNewTaskAddress('');
      await loadData();
    } catch (err) {
      if (err instanceof ApiError) {
        setErrorMsg(err.message);
      } else {
        setErrorMsg('Gagal membuat tugas pengantaran.');
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Header Banner */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-teal-50 text-teal-800 mb-2">
            <Truck className="w-3.5 h-3.5" />
            <span>Logistik Antar-Jemput (Milestone 5)</span>
          </div>
          <h2 className="text-xl font-bold text-slate-900 tracking-tight">
            {isCourier ? 'Tugas Kurir Antar-Jemput' : 'Manajemen Penjemputan & Pengantaran'}
          </h2>
          <p className="text-sm text-slate-500 mt-0.5">
            {isCourier
              ? 'Pantau pesanan yang harus dijemput atau diantar langsung ke pelanggan.'
              : 'Kelola permintaan jemput pelanggan, penugasan kurir, dan konversi ke pesanan laundry.'}
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={loadData}
            disabled={isLoading}
            className="inline-flex items-center gap-1.5 px-3.5 py-2.5 rounded-xl text-xs font-semibold text-slate-700 bg-slate-100 hover:bg-slate-200 min-h-[44px] transition-colors cursor-pointer"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${isLoading ? 'animate-spin' : ''}`} />
            <span>Segarkan</span>
          </button>
          {isCashierOrOwner && adminTab === 'tasks' && (
            <button
              onClick={() => setCreateTaskModal(true)}
              className="inline-flex items-center gap-1.5 px-3.5 py-2.5 rounded-xl text-xs font-semibold text-white bg-teal-700 hover:bg-teal-800 shadow-xs min-h-[44px] transition-colors cursor-pointer"
            >
              <Plus className="w-4 h-4" />
              <span>Tugas Pengantaran Baru</span>
            </button>
          )}
        </div>
      </div>

      {/* Notifications */}
      {errorMsg && (
        <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-800 text-sm flex items-start gap-2.5">
          <AlertCircle className="w-5 h-5 text-rose-600 shrink-0 mt-0.5" />
          <div className="flex-1">{errorMsg}</div>
          <button onClick={() => setErrorMsg(null)} className="text-rose-500 hover:text-rose-700">
            <X className="w-4 h-4" />
          </button>
        </div>
      )}

      {successMsg && (
        <div className="p-4 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-800 text-sm flex items-start gap-2.5">
          <CheckCircle2 className="w-5 h-5 text-emerald-600 shrink-0 mt-0.5" />
          <div className="flex-1">{successMsg}</div>
          <button onClick={() => setSuccessMsg(null)} className="text-emerald-500 hover:text-emerald-700">
            <X className="w-4 h-4" />
          </button>
        </div>
      )}

      {/* ============================================================== */}
      {/* COURIER VIEW: Mobile First Workflow */}
      {/* ============================================================== */}
      {isCourier && (
        <div className="space-y-4">
          {/* Segmented Filter */}
          <div className="flex gap-2 p-1 bg-slate-100 rounded-xl w-fit">
            <button
              onClick={() => setCourierFilter('ACTIVE')}
              className={`px-4 py-2 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
                courierFilter === 'ACTIVE'
                  ? 'bg-white text-slate-900 shadow-xs'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Tugas Aktif ({courierTasks.filter((t) => ['ASSIGNED', 'EN_ROUTE', 'ARRIVED'].includes(t.status)).length})
            </button>
            <button
              onClick={() => setCourierFilter('DONE')}
              className={`px-4 py-2 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
                courierFilter === 'DONE'
                  ? 'bg-white text-slate-900 shadow-xs'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Selesai ({courierTasks.filter((t) => t.status === 'COMPLETED').length})
            </button>
            <button
              onClick={() => setCourierFilter('ALL')}
              className={`px-4 py-2 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
                courierFilter === 'ALL'
                  ? 'bg-white text-slate-900 shadow-xs'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Semua ({courierTasks.length})
            </button>
          </div>

          {/* Task Cards */}
          {courierTasks
            .filter((t) => {
              if (courierFilter === 'ACTIVE') return ['ASSIGNED', 'EN_ROUTE', 'ARRIVED'].includes(t.status);
              if (courierFilter === 'DONE') return t.status === 'COMPLETED';
              return true;
            })
            .map((task) => (
              <div
                key={task.id}
                className="bg-white rounded-2xl border border-slate-200 p-5 shadow-xs space-y-4 transition hover:border-slate-300"
              >
                <div className="flex items-start justify-between gap-3">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span
                        className={`px-2.5 py-0.5 rounded-md text-xs font-bold ${
                          task.task_type === 'PICKUP'
                            ? 'bg-amber-100 text-amber-800'
                            : 'bg-teal-100 text-teal-800'
                        }`}
                      >
                        {task.task_type === 'PICKUP' ? 'PENJEMPUTAN' : 'PENGANTARAN'}
                      </span>
                      {renderTaskBadge(task.status)}
                    </div>
                    <h3 className="text-base font-bold text-slate-900 flex items-center gap-1.5 mt-1">
                      <UserIcon className="w-4 h-4 text-slate-400" />
                      {task.recipient_name || 'Pelanggan Laundry'}
                    </h3>
                  </div>
                  {task.order_number && (
                    <span className="text-xs font-mono font-bold text-slate-600 bg-slate-100 px-2.5 py-1 rounded-lg">
                      {task.order_number}
                    </span>
                  )}
                </div>

                <div className="space-y-2 text-xs text-slate-600">
                  <div className="flex items-start gap-2">
                    <MapPin className="w-4 h-4 text-rose-500 shrink-0 mt-0.5" />
                    <span className="font-medium text-slate-800">{task.destination_address}</span>
                  </div>
                  {task.destination_phone && (
                    <div className="flex items-center gap-2">
                      <Phone className="w-4 h-4 text-emerald-600 shrink-0" />
                      <span>{task.destination_phone}</span>
                    </div>
                  )}
                </div>

                {/* Mobile Quick Action Buttons */}
                <div className="pt-2 border-t border-slate-100 flex flex-wrap items-center gap-2">
                  {task.destination_phone && (
                    <a
                      href={`https://wa.me/${task.destination_phone.replace(/[^0-9]/g, '')}`}
                      target="_blank"
                      rel="noreferrer"
                      className="inline-flex items-center gap-1.5 px-3 py-2 rounded-xl text-xs font-semibold text-emerald-700 bg-emerald-50 hover:bg-emerald-100 border border-emerald-200 min-h-[44px] transition-colors"
                    >
                      <Phone className="w-3.5 h-3.5" />
                      <span>WhatsApp</span>
                    </a>
                  )}

                  <a
                    href={`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(task.destination_address)}`}
                    target="_blank"
                    rel="noreferrer"
                    className="inline-flex items-center gap-1.5 px-3 py-2 rounded-xl text-xs font-semibold text-blue-700 bg-blue-50 hover:bg-blue-100 border border-blue-200 min-h-[44px] transition-colors"
                  >
                    <Navigation className="w-3.5 h-3.5" />
                    <span>Peta Maps</span>
                  </a>

                  {/* Status Progression Workflows */}
                  {task.status === 'ASSIGNED' && (
                    <button
                      onClick={() => handleUpdateTaskStatus(task.id, 'EN_ROUTE')}
                      disabled={isSubmitting}
                      className="ml-auto inline-flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-bold text-white bg-blue-600 hover:bg-blue-700 shadow-xs min-h-[44px] cursor-pointer transition-colors"
                    >
                      <Truck className="w-3.5 h-3.5" />
                      <span>Mulai Jalan (En Route)</span>
                    </button>
                  )}

                  {task.status === 'EN_ROUTE' && (
                    <button
                      onClick={() => handleUpdateTaskStatus(task.id, 'ARRIVED')}
                      disabled={isSubmitting}
                      className="ml-auto inline-flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-bold text-white bg-indigo-600 hover:bg-indigo-700 shadow-xs min-h-[44px] cursor-pointer transition-colors"
                    >
                      <MapPin className="w-3.5 h-3.5" />
                      <span>Tiba di Lokasi</span>
                    </button>
                  )}

                  {task.status === 'ARRIVED' && (
                    <div className="ml-auto flex items-center gap-2">
                      <button
                        onClick={() => {
                          setFailTaskModal({ open: true, task });
                          setFailureReason('');
                        }}
                        className="px-3 py-2 rounded-xl text-xs font-semibold text-rose-700 bg-rose-50 hover:bg-rose-100 border border-rose-200 min-h-[44px] cursor-pointer transition-colors"
                      >
                        Kendala / Gagal
                      </button>
                      <button
                        onClick={() => {
                          if (task.task_type === 'PICKUP') {
                            handleUpdateTaskStatus(task.id, 'COMPLETED');
                          } else {
                            setCompleteTaskModal({ open: true, task });
                            setRecipientName(task.recipient_name || '');
                            setCompletionNotes('');
                          }
                        }}
                        disabled={isSubmitting}
                        className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-bold text-white bg-emerald-600 hover:bg-emerald-700 shadow-xs min-h-[44px] cursor-pointer transition-colors"
                      >
                        <CheckCircle2 className="w-3.5 h-3.5" />
                        <span>{task.task_type === 'PICKUP' ? 'Selesai Dijemput' : 'Serahkan ke Pelanggan'}</span>
                      </button>
                    </div>
                  )}

                  {task.status === 'COMPLETED' && (
                    <div className="ml-auto text-xs font-semibold text-emerald-700 flex items-center gap-1">
                      <CheckCircle2 className="w-4 h-4" />
                      <span>Tugas Selesai</span>
                    </div>
                  )}
                </div>
              </div>
            ))}

          {courierTasks.length === 0 && !isLoading && (
            <div className="p-12 text-center bg-white rounded-2xl border border-slate-200 shadow-xs">
              <Truck className="w-12 h-12 text-slate-300 mx-auto mb-3" />
              <h3 className="text-base font-bold text-slate-900">Belum Ada Tugas Ditugaskan</h3>
              <p className="text-sm text-slate-500 mt-1 max-w-sm mx-auto">
                Saat kasir menugaskan penjemputan atau pengantaran pesanan, tugas Anda akan muncul di sini.
              </p>
            </div>
          )}
        </div>
      )}

      {/* ============================================================== */}
      {/* CASHIER & OWNER VIEW: Full Logistics Control */}
      {/* ============================================================== */}
      {isCashierOrOwner && (
        <div className="space-y-6">
          {/* Sub Navigation */}
          <div className="border-b border-slate-200">
            <nav className="flex gap-4">
              <button
                onClick={() => setAdminTab('pickups')}
                className={`pb-3 text-sm font-bold border-b-2 transition-colors cursor-pointer ${
                  adminTab === 'pickups'
                    ? 'border-teal-700 text-teal-800'
                    : 'border-transparent text-slate-500 hover:text-slate-800'
                }`}
              >
                Permintaan Jemput ({pickups.length})
              </button>
              <button
                onClick={() => setAdminTab('tasks')}
                className={`pb-3 text-sm font-bold border-b-2 transition-colors cursor-pointer ${
                  adminTab === 'tasks'
                    ? 'border-teal-700 text-teal-800'
                    : 'border-transparent text-slate-500 hover:text-slate-800'
                }`}
              >
                Semua Tugas Kurir ({allTasks.length})
              </button>
            </nav>
          </div>

          {/* TAB 1: PICKUP REQUESTS */}
          {adminTab === 'pickups' && (
            <div className="space-y-4">
              {/* Pickup Filter */}
              <div className="flex flex-wrap items-center justify-between gap-3 bg-white p-3 rounded-2xl border border-slate-200 shadow-xs">
                <div className="flex items-center gap-2 text-xs">
                  <span className="font-semibold text-slate-500">Filter Status:</span>
                  <select
                    value={pickupFilter}
                    onChange={(e) => setPickupFilter(e.target.value)}
                    className="px-3 py-1.5 rounded-lg border border-slate-300 bg-white text-slate-800 text-xs focus:ring-2 focus:ring-teal-500 focus:outline-hidden"
                  >
                    <option value="">Semua Status</option>
                    <option value="REQUESTED">Menunggu Konfirmasi (REQUESTED)</option>
                    <option value="ASSIGNED">Kurir Ditugaskan (ASSIGNED)</option>
                    <option value="PICKED_UP">Sudah Dijemput (PICKED_UP)</option>
                    <option value="CONVERTED">Dikonversi Pesanan (CONVERTED)</option>
                    <option value="CANCELLED">Dibatalkan</option>
                  </select>
                </div>
              </div>

              {/* Pickup Cards Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {pickups
                  .filter((p) => !pickupFilter || p.status === pickupFilter)
                  .map((pickup) => (
                    <div
                      key={pickup.id}
                      className="bg-white rounded-2xl border border-slate-200 p-5 shadow-xs space-y-4 flex flex-col justify-between"
                    >
                      <div className="space-y-3">
                        <div className="flex items-start justify-between gap-2">
                          <div>
                            <span className="font-mono text-xs font-bold text-teal-800 bg-teal-50 px-2 py-0.5 rounded-md border border-teal-100">
                              {pickup.request_number}
                            </span>
                            <h3 className="text-base font-bold text-slate-900 mt-1">
                              {pickup.requester_name}
                            </h3>
                          </div>
                          {renderPickupBadge(pickup.status)}
                        </div>

                        <div className="space-y-1.5 text-xs text-slate-600">
                          <div className="flex items-start gap-2">
                            <MapPin className="w-4 h-4 text-rose-500 shrink-0 mt-0.5" />
                            <span>{pickup.pickup_address}</span>
                          </div>
                          <div className="flex items-center gap-2">
                            <Phone className="w-4 h-4 text-emerald-600 shrink-0" />
                            <span>{pickup.phone_e164}</span>
                          </div>
                          <div className="flex items-center gap-2">
                            <Calendar className="w-4 h-4 text-slate-400 shrink-0" />
                            <span>
                              {pickup.requested_date} ({pickup.requested_time_start.slice(0, 5)} -{' '}
                              {pickup.requested_time_end.slice(0, 5)})
                            </span>
                          </div>
                          {pickup.notes && (
                            <div className="p-2.5 rounded-lg bg-slate-50 border border-slate-100 text-slate-700 italic">
                              "{pickup.notes}"
                            </div>
                          )}
                        </div>
                      </div>

                      {/* Cashier Action Controls */}
                      <div className="pt-3 border-t border-slate-100 flex flex-wrap items-center justify-between gap-2">
                        {pickup.tracking_url && (
                          <a
                            href={pickup.tracking_url}
                            target="_blank"
                            rel="noreferrer"
                            className="inline-flex items-center gap-1.5 px-3 py-2 rounded-xl text-xs text-teal-700 hover:text-teal-900 bg-teal-50 hover:bg-teal-100 font-semibold min-h-[44px] transition-colors"
                          >
                            <ExternalLink className="w-3.5 h-3.5" />
                            <span>Tracking Publik</span>
                          </a>
                        )}

                        <div className="flex items-center gap-2 ml-auto">
                          {pickup.status === 'REQUESTED' && (
                            <>
                              <button
                                onClick={() => {
                                  setRejectModal({ open: true, pickup });
                                  setRejectReason('');
                                }}
                                className="px-3 py-1.5 rounded-xl text-xs font-semibold text-rose-700 bg-rose-50 hover:bg-rose-100 border border-rose-200 cursor-pointer"
                              >
                                Tolak
                              </button>
                              <button
                                onClick={() => openConfirmModal(pickup)}
                                className="px-3.5 py-1.5 rounded-xl text-xs font-bold text-white bg-teal-700 hover:bg-teal-800 shadow-xs cursor-pointer"
                              >
                                Konfirmasi & Kurir
                              </button>
                            </>
                          )}

                          {pickup.status === 'PICKED_UP' && (
                            <button
                              onClick={() => openConvertModal(pickup)}
                              className="inline-flex items-center gap-1 px-4 py-2 rounded-xl text-xs font-bold text-white bg-emerald-600 hover:bg-emerald-700 shadow-xs cursor-pointer"
                            >
                              <Plus className="w-3.5 h-3.5" />
                              <span>Konversi ke Pesanan (DEC-10)</span>
                            </button>
                          )}

                          {pickup.status === 'CONVERTED' && (
                            <span className="text-xs font-semibold text-teal-800 bg-teal-50 px-2.5 py-1 rounded-lg border border-teal-100">
                              Sudah Menjadi Order
                            </span>
                          )}
                        </div>
                      </div>
                    </div>
                  ))}

                {pickups.length === 0 && !isLoading && (
                  <div className="col-span-2 p-12 text-center bg-white rounded-2xl border border-slate-200 shadow-xs">
                    <Package className="w-12 h-12 text-slate-300 mx-auto mb-3" />
                    <h3 className="text-base font-bold text-slate-900">Belum Ada Permintaan Penjemputan</h3>
                    <p className="text-sm text-slate-500 mt-1 max-w-sm mx-auto">
                      Permintaan jemput yang diajukan pelanggan melalui portal publik akan muncul di sini.
                    </p>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* TAB 2: ALL DELIVERY TASKS */}
          {adminTab === 'tasks' && (
            <div className="space-y-4">
              {/* Task Filter */}
              <div className="flex flex-wrap items-center justify-between gap-3 bg-white p-3 rounded-2xl border border-slate-200 shadow-xs">
                <div className="flex items-center gap-2 text-xs">
                  <span className="font-semibold text-slate-500">Filter Status:</span>
                  <select
                    value={taskFilter}
                    onChange={(e) => setTaskFilter(e.target.value)}
                    className="px-3 py-1.5 rounded-lg border border-slate-300 bg-white text-slate-800 text-xs focus:ring-2 focus:ring-teal-500 focus:outline-hidden"
                  >
                    <option value="">Semua Status</option>
                    <option value="ASSIGNED">Ditugaskan (ASSIGNED)</option>
                    <option value="EN_ROUTE">Dalam Perjalanan (EN_ROUTE)</option>
                    <option value="ARRIVED">Tiba di Lokasi (ARRIVED)</option>
                    <option value="COMPLETED">Selesai (COMPLETED)</option>
                    <option value="FAILED">Gagal (FAILED)</option>
                  </select>
                </div>
              </div>

              {/* Tasks Table */}
              <div className="bg-white rounded-2xl border border-slate-200 shadow-xs overflow-hidden">
                <div className="overflow-x-auto">
                  <table className="w-full text-left text-xs text-slate-600">
                    <thead className="bg-slate-50 text-slate-700 font-semibold border-b border-slate-200 uppercase tracking-wider text-[11px]">
                      <tr>
                        <th className="px-4 py-3">Tipe</th>
                        <th className="px-4 py-3">Penerima / Alamat</th>
                        <th className="px-4 py-3">Kurir</th>
                        <th className="px-4 py-3">Status</th>
                        <th className="px-4 py-3">Dibuat Pada</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100">
                      {allTasks
                        .filter((t) => !taskFilter || t.status === taskFilter)
                        .map((task) => (
                          <tr key={task.id} className="hover:bg-slate-50/60 transition-colors">
                            <td className="px-4 py-3">
                              <span
                                className={`px-2 py-0.5 rounded-md font-bold text-[11px] ${
                                  task.task_type === 'PICKUP'
                                    ? 'bg-amber-100 text-amber-800'
                                    : 'bg-teal-100 text-teal-800'
                                }`}
                              >
                                {task.task_type}
                              </span>
                            </td>
                            <td className="px-4 py-3 space-y-0.5">
                              <div className="font-bold text-slate-900">{task.recipient_name || '-'}</div>
                              <div className="text-slate-500 max-w-xs truncate">{task.destination_address}</div>
                            </td>
                            <td className="px-4 py-3 font-medium text-slate-800">
                              {task.courier_name || <span className="text-slate-400 italic">Belum Ditugaskan</span>}
                            </td>
                            <td className="px-4 py-3">{renderTaskBadge(task.status)}</td>
                            <td className="px-4 py-3 text-slate-500">
                              {new Date(task.created_at).toLocaleString('id-ID', {
                                dateStyle: 'short',
                                timeStyle: 'short',
                              })}
                            </td>
                          </tr>
                        ))}

                      {allTasks.length === 0 && !isLoading && (
                        <tr>
                          <td colSpan={5} className="px-4 py-8 text-center text-slate-400">
                            Belum ada tugas pengantaran atau penjemputan.
                          </td>
                        </tr>
                      )}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* ============================================================== */}
      {/* MODAL 1: Confirm & Assign Courier */}
      {/* ============================================================== */}
      {assignModal.open && assignModal.pickup && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-xs">
          <div className="bg-white rounded-2xl max-w-md w-full p-6 shadow-xl space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-base font-bold text-slate-900">
                Konfirmasi Penjemputan #{assignModal.pickup.request_number}
              </h3>
              <button
                onClick={() => setAssignModal({ open: false, pickup: null })}
                className="text-slate-400 hover:text-slate-600"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleSubmitConfirm} noValidate className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Waktu Mulai Dijemput
                </label>
                <input
                  type="datetime-local"
                  required
                  value={confirmStartAt}
                  onChange={(e) => setConfirmStartAt(e.target.value)}
                  className="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs focus:ring-2 focus:ring-teal-500 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Waktu Selesai Dijemput
                </label>
                <input
                  type="datetime-local"
                  required
                  value={confirmEndAt}
                  onChange={(e) => setConfirmEndAt(e.target.value)}
                  className="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs focus:ring-2 focus:ring-teal-500 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Pilih Kurir Penjemput
                </label>
                <select
                  value={selectedCourierId}
                  onChange={(e) => setSelectedCourierId(e.target.value)}
                  className="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs bg-white focus:ring-2 focus:ring-teal-500 focus:outline-hidden"
                >
                  <option value="">-- Tanpa Penugasan Otomatis --</option>
                  {couriers.map((c) => (
                    <option key={c.id} value={c.id}>
                      {c.full_name} (@{c.username})
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Catatan untuk Kurir
                </label>
                <textarea
                  rows={2}
                  value={assignNotes}
                  onChange={(e) => setAssignNotes(e.target.value)}
                  placeholder="Misal: Ambil di pos satpam depan perumahan"
                  className="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs focus:ring-2 focus:ring-teal-500 focus:outline-hidden"
                />
              </div>

              <div className="flex items-center justify-end gap-2 pt-2">
                <button
                  type="button"
                  onClick={() => setAssignModal({ open: false, pickup: null })}
                  className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-600 hover:bg-slate-100"
                >
                  Batal
                </button>
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="px-4 py-2 rounded-xl text-xs font-bold text-white bg-teal-700 hover:bg-teal-800 disabled:opacity-50 cursor-pointer"
                >
                  {isSubmitting ? 'Menyimpan...' : 'Konfirmasi & Kirim Kurir'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* ============================================================== */}
      {/* MODAL 2: Reject Pickup Request */}
      {/* ============================================================== */}
      {rejectModal.open && rejectModal.pickup && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-xs">
          <div className="bg-white rounded-2xl max-w-sm w-full p-6 shadow-xl space-y-4">
            <h3 className="text-base font-bold text-slate-900">
              Tolak Permintaan Penjemputan
            </h3>
            <p className="text-xs text-slate-500">
              Pelanggan akan melihat alasan penolakan ini di halaman tracking publik.
            </p>

            <form onSubmit={handleSubmitReject} noValidate className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Alasan Penolakan
                </label>
                <textarea
                  rows={3}
                  required
                  value={rejectReason}
                  onChange={(e) => setRejectReason(e.target.value)}
                  placeholder="Misal: Lokasi penjemputan berada di luar jangkauan kurir kami."
                  className="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs focus:ring-2 focus:ring-rose-500 focus:outline-hidden"
                />
              </div>

              <div className="flex items-center justify-end gap-2 pt-2">
                <button
                  type="button"
                  onClick={() => setRejectModal({ open: false, pickup: null })}
                  className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-600 hover:bg-slate-100"
                >
                  Batal
                </button>
                <button
                  type="submit"
                  disabled={isSubmitting || rejectReason.length < 3}
                  className="px-4 py-2 rounded-xl text-xs font-bold text-white bg-rose-600 hover:bg-rose-700 disabled:opacity-50 cursor-pointer"
                >
                  {isSubmitting ? 'Memproses...' : 'Tolak Permintaan'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* ============================================================== */}
      {/* MODAL 3: Convert Pickup to Order (DEC-10) */}
      {/* ============================================================== */}
      {convertModal.open && convertModal.pickup && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-xs">
          <div className="bg-white rounded-2xl max-w-md w-full p-6 shadow-xl space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-base font-bold text-slate-900">
                  Konversi Penjemputan ke Pesanan Laundry
                </h3>
                <p className="text-xs text-slate-500 mt-0.5">
                  Pelanggan: <strong className="text-slate-800">{convertModal.pickup.requester_name}</strong>
                </p>
              </div>
              <button
                onClick={() => setConvertModal({ open: false, pickup: null })}
                className="text-slate-400 hover:text-slate-600"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleSubmitConvert} noValidate className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Layanan Laundry
                </label>
                <select
                  value={convertServiceId}
                  onChange={(e) => setConvertServiceId(e.target.value)}
                  className="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs bg-white focus:ring-2 focus:ring-teal-500 focus:outline-hidden"
                >
                  {services.map((s) => (
                    <option key={s.id} value={s.id}>
                      {s.name} (Rp {s.unit_price.toLocaleString('id-ID')} / {s.unit})
                    </option>
                  ))}
                </select>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1">
                    Berat / Jumlah
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    min="0.1"
                    required
                    value={convertQuantity}
                    onChange={(e) => setConvertQuantity(e.target.value)}
                    className="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs focus:ring-2 focus:ring-teal-500 focus:outline-hidden"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1">
                    Ongkos Antar (Rp)
                  </label>
                  <input
                    type="number"
                    min="0"
                    step="1000"
                    value={convertDeliveryFee}
                    onChange={(e) => setConvertDeliveryFee(e.target.value)}
                    className="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs focus:ring-2 focus:ring-teal-500 focus:outline-hidden"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Metode Pengembalian Cucian
                </label>
                <div className="grid grid-cols-2 gap-2">
                  <button
                    type="button"
                    onClick={() => setConvertReturnMethod('SELF_PICKUP')}
                    className={`py-2 px-3 rounded-xl text-xs font-bold border transition-colors cursor-pointer ${
                      convertReturnMethod === 'SELF_PICKUP'
                        ? 'border-teal-700 bg-teal-50 text-teal-900'
                        : 'border-slate-200 text-slate-600 hover:bg-slate-50'
                    }`}
                  >
                    Ambil Mandiri
                  </button>
                  <button
                    type="button"
                    onClick={() => setConvertReturnMethod('HOME_DELIVERY')}
                    className={`py-2 px-3 rounded-xl text-xs font-bold border transition-colors cursor-pointer ${
                      convertReturnMethod === 'HOME_DELIVERY'
                        ? 'border-teal-700 bg-teal-50 text-teal-900'
                        : 'border-slate-200 text-slate-600 hover:bg-slate-50'
                    }`}
                  >
                    Antar ke Rumah
                  </button>
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Catatan Cucian
                </label>
                <textarea
                  rows={2}
                  value={convertNotes}
                  onChange={(e) => setConvertNotes(e.target.value)}
                  placeholder="Misal: Jangan gunakan pemutih untuk baju warna"
                  className="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs focus:ring-2 focus:ring-teal-500 focus:outline-hidden"
                />
              </div>

              <div className="flex items-center justify-end gap-2 pt-2">
                <button
                  type="button"
                  onClick={() => setConvertModal({ open: false, pickup: null })}
                  className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-600 hover:bg-slate-100"
                >
                  Batal
                </button>
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="px-4 py-2 rounded-xl text-xs font-bold text-white bg-emerald-600 hover:bg-emerald-700 disabled:opacity-50 cursor-pointer"
                >
                  {isSubmitting ? 'Membuat Order...' : 'Buat Pesanan Laundry'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* ============================================================== */}
      {/* MODAL 4: Courier Complete Delivery */}
      {/* ============================================================== */}
      {completeTaskModal.open && completeTaskModal.task && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-xs">
          <div className="bg-white rounded-2xl max-w-sm w-full p-6 shadow-xl space-y-4">
            <h3 className="text-base font-bold text-slate-900">
              Konfirmasi Penyerahan Cucian
            </h3>
            <p className="text-xs text-slate-500">
              Pastikan cucian telah diterima langsung oleh pelanggan atau pihak yang berhak.
            </p>

            <form
              onSubmit={(e) => {
                e.preventDefault();
                if (!completeTaskModal.task) return;
                handleUpdateTaskStatus(completeTaskModal.task.id, 'COMPLETED', {
                  received_by_name: recipientName,
                  notes: completionNotes,
                });
                setCompleteTaskModal({ open: false, task: null });
              }}
              noValidate
              className="space-y-4"
            >
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Nama Penerima
                </label>
                <input
                  type="text"
                  required
                  value={recipientName}
                  onChange={(e) => setRecipientName(e.target.value)}
                  placeholder="Misal: Ibu Ani (Pribadi)"
                  className="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs focus:ring-2 focus:ring-teal-500 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Catatan Serah Terima
                </label>
                <textarea
                  rows={2}
                  value={completionNotes}
                  onChange={(e) => setCompletionNotes(e.target.value)}
                  placeholder="Misal: Diterima langsung dan dititipkan di meja depan."
                  className="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs focus:ring-2 focus:ring-teal-500 focus:outline-hidden"
                />
              </div>

              <div className="flex items-center justify-end gap-2 pt-2">
                <button
                  type="button"
                  onClick={() => setCompleteTaskModal({ open: false, task: null })}
                  className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-600 hover:bg-slate-100"
                >
                  Batal
                </button>
                <button
                  type="submit"
                  disabled={isSubmitting || !recipientName.trim()}
                  className="px-4 py-2 rounded-xl text-xs font-bold text-white bg-emerald-600 hover:bg-emerald-700 disabled:opacity-50 cursor-pointer"
                >
                  Konfirmasi Selesai
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* ============================================================== */}
      {/* MODAL 5: Courier Fail Task */}
      {/* ============================================================== */}
      {failTaskModal.open && failTaskModal.task && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-xs">
          <div className="bg-white rounded-2xl max-w-sm w-full p-6 shadow-xl space-y-4">
            <h3 className="text-base font-bold text-slate-900">
              Laporkan Kendala Tugas
            </h3>

            <form
              onSubmit={(e) => {
                e.preventDefault();
                if (!failTaskModal.task) return;
                handleUpdateTaskStatus(failTaskModal.task.id, 'FAILED', {
                  failure_reason: failureReason,
                });
                setFailTaskModal({ open: false, task: null });
              }}
              noValidate
              className="space-y-4"
            >
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Penyebab Kendala / Gagal
                </label>
                <textarea
                  rows={3}
                  required
                  value={failureReason}
                  onChange={(e) => setFailureReason(e.target.value)}
                  placeholder="Misal: Rumah kosong, nomor telepon pelanggan tidak dapat dihubungi setelah 3x panggilan."
                  className="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs focus:ring-2 focus:ring-rose-500 focus:outline-hidden"
                />
              </div>

              <div className="flex items-center justify-end gap-2 pt-2">
                <button
                  type="button"
                  onClick={() => setFailTaskModal({ open: false, task: null })}
                  className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-600 hover:bg-slate-100"
                >
                  Batal
                </button>
                <button
                  type="submit"
                  disabled={isSubmitting || failureReason.length < 5}
                  className="px-4 py-2 rounded-xl text-xs font-bold text-white bg-rose-600 hover:bg-rose-700 disabled:opacity-50 cursor-pointer"
                >
                  Kirim Laporan
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* ============================================================== */}
      {/* MODAL 6: Create New Delivery Task (Cashier) */}
      {/* ============================================================== */}
      {createTaskModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-xs">
          <div className="bg-white rounded-2xl max-w-md w-full p-6 shadow-xl space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-base font-bold text-slate-900">
                Buat Tugas Pengantaran Baru
              </h3>
              <button
                onClick={() => setCreateTaskModal(false)}
                className="text-slate-400 hover:text-slate-600"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleCreateTask} noValidate className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Nama Penerima
                </label>
                <input
                  type="text"
                  required
                  value={newTaskRecipient}
                  onChange={(e) => setNewTaskRecipient(e.target.value)}
                  placeholder="Misal: Budi Santoso"
                  className="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs focus:ring-2 focus:ring-teal-500 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Nomor Telepon
                </label>
                <input
                  type="tel"
                  value={newTaskPhone}
                  onChange={(e) => setNewTaskPhone(e.target.value)}
                  placeholder="Misal: 081234567890"
                  className="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs focus:ring-2 focus:ring-teal-500 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Alamat Pengantaran
                </label>
                <textarea
                  rows={2}
                  required
                  value={newTaskAddress}
                  onChange={(e) => setNewTaskAddress(e.target.value)}
                  placeholder="Jl. Sukajadi No. 12, Bandung"
                  className="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs focus:ring-2 focus:ring-teal-500 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Tugaskan ke Kurir
                </label>
                <select
                  value={newTaskCourierId}
                  onChange={(e) => setNewTaskCourierId(e.target.value)}
                  className="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs bg-white focus:ring-2 focus:ring-teal-500 focus:outline-hidden"
                >
                  <option value="">-- Tanpa Penugasan Langsung --</option>
                  {couriers.map((c) => (
                    <option key={c.id} value={c.id}>
                      {c.full_name} (@{c.username})
                    </option>
                  ))}
                </select>
              </div>

              <div className="flex items-center justify-end gap-2 pt-2">
                <button
                  type="button"
                  onClick={() => setCreateTaskModal(false)}
                  className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-600 hover:bg-slate-100"
                >
                  Batal
                </button>
                <button
                  type="submit"
                  disabled={isSubmitting || !newTaskAddress.trim()}
                  className="px-4 py-2 rounded-xl text-xs font-bold text-white bg-teal-700 hover:bg-teal-800 disabled:opacity-50 cursor-pointer"
                >
                  {isSubmitting ? 'Menyimpan...' : 'Buat Tugas'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
export default DeliveryPage;
