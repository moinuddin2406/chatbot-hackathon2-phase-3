// src/utils/date-utils.ts
// Utility functions for date formatting

export function formatDate(dateString: string | undefined): string {
  if (!dateString) return "—";
  const d = new Date(dateString);
  if (isNaN(d.getTime())) return "—";
  return d.toLocaleDateString();
}

export function formatDateOnly(dateString: string | undefined): string {
  if (!dateString) return "—";
  const d = new Date(dateString);
  if (isNaN(d.getTime())) return "—";
  return d.toLocaleDateString();
}

// Additional utility function to format datetime in a more readable way
export function formatDateTime(dateString: string | undefined): string {
  if (!dateString) return "—";
  const d = new Date(dateString);
  if (isNaN(d.getTime())) return "—";
  return d.toLocaleDateString();
}