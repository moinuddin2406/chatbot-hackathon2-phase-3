export default function Loading() {
  // You can add a loading spinner or skeleton here
  return (
    <div className="flex items-center justify-center min-h-screen bg-[#0b0b12]">
      <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-theme-primary"></div>
    </div>
  );
}