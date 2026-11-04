import React from 'react';
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { EmptyState } from '../ui/empty-state';
import { LoadingSpinner } from '../ui/loading-spinner';

describe('UI Component Library Tests (FE-02)', () => {
  describe('Button Component', () => {
    it('renders with children text and triggers onClick', () => {
      const handleClick = vi.fn();
      render(<Button onClick={handleClick}>Simpan Pesanan</Button>);

      const btn = screen.getByRole('button', { name: /Simpan Pesanan/i });
      expect(btn).toBeInTheDocument();
      fireEvent.click(btn);
      expect(handleClick).toHaveBeenCalledTimes(1);
    });

    it('enforces accessible tap target styles (min-h-[44px] min-w-[44px])', () => {
      render(<Button>Touch Target</Button>);
      const btn = screen.getByRole('button', { name: /Touch Target/i });
      expect(btn.className).toContain('min-h-[44px]');
      expect(btn.className).toContain('min-w-[44px]');
    });

    it('shows loading indicator and disables button when isLoading is true', () => {
      const handleClick = vi.fn();
      render(
        <Button isLoading onClick={handleClick}>
          Simpan Pesanan
        </Button>
      );

      const btn = screen.getByRole('button');
      expect(btn).toBeDisabled();
      expect(screen.getByTestId('loading-indicator')).toBeInTheDocument();
      expect(screen.getByText('Memproses...')).toBeInTheDocument();

      fireEvent.click(btn);
      expect(handleClick).not.toHaveBeenCalled();
    });

    it('disables button when disabled prop is passed', () => {
      const handleClick = vi.fn();
      render(
        <Button disabled onClick={handleClick}>
          Disabled Button
        </Button>
      );
      const btn = screen.getByRole('button');
      expect(btn).toBeDisabled();
      fireEvent.click(btn);
      expect(handleClick).not.toHaveBeenCalled();
    });
  });

  describe('Badge Component', () => {
    it('renders text with appropriate styling classes', () => {
      render(<Badge variant="success">LUNAS</Badge>);
      const badge = screen.getByText('LUNAS');
      expect(badge).toBeInTheDocument();
      expect(badge.className).toContain('bg-emerald-50');
      expect(badge.className).toContain('text-emerald-700');
    });

    it('renders danger variant for UNPAID', () => {
      render(<Badge variant="danger">BELUM LUNAS</Badge>);
      const badge = screen.getByText('BELUM LUNAS');
      expect(badge.className).toContain('bg-rose-50');
      expect(badge.className).toContain('text-rose-700');
    });
  });

  describe('EmptyState Component', () => {
    it('renders title, description, and action button', () => {
      render(
        <EmptyState
          title="Tidak Ada Pesanan"
          description="Belum ada pesanan aktif hari ini."
          action={<Button>Buat Pesanan Baru</Button>}
        />
      );

      expect(screen.getByText('Tidak Ada Pesanan')).toBeInTheDocument();
      expect(screen.getByText('Belum ada pesanan aktif hari ini.')).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /Buat Pesanan Baru/i })).toBeInTheDocument();
    });
  });

  describe('LoadingSpinner Component', () => {
    it('renders accessible live region with label', () => {
      render(<LoadingSpinner label="Memuat data transaksi..." />);
      const region = screen.getByRole('status');
      expect(region).toBeInTheDocument();
      expect(screen.getAllByText('Memuat data transaksi...').length).toBeGreaterThan(0);
    });
  });
});

