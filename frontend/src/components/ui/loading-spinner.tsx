import React from 'react';
import { cn } from '../../lib/utils';

export interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  className?: string;
  label?: string;
}

export function LoadingSpinner({ size = 'md', className, label = 'Memuat...' }: LoadingSpinnerProps) {
  const sizes = {
    sm: 'h-4 w-4 border-2',
    md: 'h-8 w-8 border-3',
    lg: 'h-12 w-12 border-4',
  };

  return (
    <div className="flex flex-col items-center justify-center gap-2 p-4" role="status" aria-live="polite">
      <div
        className={cn(
          'animate-spin rounded-full border-blue-600 border-t-transparent',
          sizes[size],
          className
        )}
      />
      {label && <span className="text-xs font-medium text-slate-500">{label}</span>}
      <span className="sr-only">{label}</span>
    </div>
  );
}

