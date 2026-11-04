import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]): string {
  return twMerge(clsx(inputs));
}

/**
 * Format a numeric amount to Indonesian Rupiah representation (e.g. Rp 10.000).
 */
export function formatRupiah(amount: number): string {
  if (isNaN(amount) || amount === null || amount === undefined) {
    return 'Rp 0';
  }
  return new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency: 'IDR',
    maximumFractionDigits: 0,
  }).format(amount).replace(/\s/g, ' ');
}

/**
 * Normalizes an Indonesian phone number string into E.164 format (+62...).
 * Example: '08123456789' -> '+628123456789'
 */
export function normalizePhoneE164(phone: string): string {
  if (!phone) return '';
  const digits = phone.replace(/\D/g, '');
  if (digits.startsWith('62')) {
    return `+${digits}`;
  }
  if (digits.startsWith('0')) {
    return `+62${digits.slice(1)}`;
  }
  if (digits.length >= 8) {
    return `+62${digits}`;
  }
  return phone;
}

/**
 * Format ISO datetime string into human readable Indonesian date/time.
 */
export function formatDateTime(isoString: string | null | undefined): string {
  if (!isoString) return '-';
  try {
    const d = new Date(isoString);
    if (isNaN(d.getTime())) return '-';
    return new Intl.DateTimeFormat('id-ID', {
      day: 'numeric',
      month: 'short',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    }).format(d);
  } catch {
    return '-';
  }
}

/**
 * Calculate total price breakdown for order intake items.
 */
export function calculateOrderBreakdown(
  items: Array<{ unitPrice: number; quantity: number }>,
  extraCharge = 0,
  deliveryFee = 0
): { subtotal: number; grandTotal: number } {
  const subtotal = items.reduce((acc, it) => acc + Math.round(it.unitPrice * it.quantity), 0);
  const grandTotal = Math.max(0, subtotal + Math.max(0, extraCharge) + Math.max(0, deliveryFee));
  return { subtotal, grandTotal };
}

