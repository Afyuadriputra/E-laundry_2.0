import { describe, it, expect } from 'vitest';
import {
  cn,
  formatRupiah,
  normalizePhoneE164,
  formatDateTime,
  calculateOrderBreakdown,
} from '../utils';

describe('Frontend Pure Utility Functions (FE-01)', () => {
  describe('cn (Tailwind class merging)', () => {
    it('merges class names and handles conflicting tailwind classes', () => {
      const result = cn('px-2 py-1', 'bg-blue-500', 'px-4');
      expect(result).toContain('px-4');
      expect(result).not.toContain('px-2');
      expect(result).toContain('bg-blue-500');
    });

    it('ignores falsy values', () => {
      expect(cn('btn', false && 'btn-active', null, undefined, 'btn-primary')).toBe(
        'btn btn-primary'
      );
    });
  });

  describe('formatRupiah', () => {
    it('formats integer amounts into IDR currency style', () => {
      const formatted = formatRupiah(10000);
      expect(formatted).toContain('10.000');
      expect(formatted).toContain('Rp');
    });

    it('handles zero and invalid inputs gracefully', () => {
      expect(formatRupiah(0)).toContain('0');
      // @ts-expect-error testing invalid input
      expect(formatRupiah(null)).toBe('Rp 0');
      // @ts-expect-error testing invalid input
      expect(formatRupiah(undefined)).toBe('Rp 0');
    });
  });

  describe('normalizePhoneE164', () => {
    it('normalizes 08xx to +628xx', () => {
      expect(normalizePhoneE164('081234567890')).toBe('+6281234567890');
    });

    it('preserves existing +62 numbers', () => {
      expect(normalizePhoneE164('+6281234567890')).toBe('+6281234567890');
    });

    it('handles numbers starting with 62 without plus', () => {
      expect(normalizePhoneE164('6281234567890')).toBe('+6281234567890');
    });

    it('strips dashes, spaces, and punctuation', () => {
      expect(normalizePhoneE164('0812-3456 7890')).toBe('+6281234567890');
    });

    it('returns empty string for empty input', () => {
      expect(normalizePhoneE164('')).toBe('');
    });
  });

  describe('formatDateTime', () => {
    it('formats ISO date string into Indonesian readable date', () => {
      const formatted = formatDateTime('2026-11-04T10:00:00Z');
      expect(formatted).not.toBe('-');
      expect(formatted).toContain('2026');
    });

    it('returns - for null, undefined, or invalid date strings', () => {
      expect(formatDateTime(null)).toBe('-');
      expect(formatDateTime(undefined)).toBe('-');
      expect(formatDateTime('invalid-date-format')).toBe('-');
    });
  });

  describe('calculateOrderBreakdown', () => {
    it('calculates subtotal and grandTotal with extra charges and delivery fee', () => {
      const items = [
        { unitPrice: 10000, quantity: 3.5 }, // 35,000
        { unitPrice: 30000, quantity: 1.0 }, // 30,000
      ];
      const result = calculateOrderBreakdown(items, 5000, 10000);
      expect(result.subtotal).toBe(65000);
      expect(result.grandTotal).toBe(80000);
    });

    it('handles zero extra charges and delivery fee', () => {
      const items = [{ unitPrice: 8000, quantity: 2 }];
      const result = calculateOrderBreakdown(items);
      expect(result.subtotal).toBe(16000);
      expect(result.grandTotal).toBe(16000);
    });

    it('handles empty item list', () => {
      const result = calculateOrderBreakdown([]);
      expect(result.subtotal).toBe(0);
      expect(result.grandTotal).toBe(0);
    });
  });
});

