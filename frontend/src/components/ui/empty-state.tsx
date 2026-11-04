import React from 'react';
import { cn } from '../../lib/utils';

export interface EmptyStateProps {
  title: string;
  description?: string;
  action?: React.ReactNode;
  icon?: React.ReactNode;
  className?: string;
}

export function EmptyState({ title, description, action, icon, className }: EmptyStateProps) {
  return (
    <div
      className={cn(
        'flex flex-col items-center justify-center p-8 text-center bg-white rounded-xl border border-dashed border-slate-300',
        className
      )}
      role="status"
    >
      {icon && <div className="mb-4 text-slate-400">{icon}</div>}
      <h3 className="text-base font-semibold text-slate-800">{title}</h3>
      {description && <p className="mt-1 text-sm text-slate-500 max-w-sm">{description}</p>}
      {action && <div className="mt-4">{action}</div>}
    </div>
  );
}

