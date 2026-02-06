'use client';

import React, { useState } from 'react';
import { useAuth } from '@/context/auth-context';
import { useRouter } from 'next/navigation';

interface Field {
  name: string;
  label: string;
  type: string;
  required: boolean;
}

interface AuthFormProps {
  title: string;
  fields: Field[];
  submitButtonText: string;
  isLoading: boolean;
  errorMessage: string | null;
  onSubmit: (formData: Record<string, string>) => Promise<void>;
  onToggleForm?: () => void;
  toggleText?: string;
}

export default function AuthForm({
  title,
  fields,
  submitButtonText,
  isLoading,
  errorMessage,
  onSubmit,
  onToggleForm,
  toggleText,
}: AuthFormProps) {
  const [formData, setFormData] = useState<Record<string, string>>({});
  const [localError, setLocalError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLocalError(null);

    try {
      await onSubmit(formData);
    } catch (error: any) {
      setLocalError(error.message || 'An error occurred during authentication');
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  return (
    <div className="flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-sm">
        <h2 className="mt-10 text-center text-2xl font-bold leading-9 tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-[#3bdcff] to-[#38bdf8] neon-glow">
          {title}
        </h2>
      </div>

      <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
        <form className="space-y-6" onSubmit={handleSubmit}>
          {fields.map((field) => (
            <div key={field.name}>
              <label
                htmlFor={field.name}
                className="block text-sm font-medium leading-6 text-[#e5e7eb] neon-glow"
              >
                {field.label}
              </label>
              <div className="mt-2">
                <input
                  id={field.name}
                  name={field.name}
                  type={field.type}
                  required={field.required}
                  value={formData[field.name] || ''}
                  onChange={handleChange}
                  disabled={isLoading}
                  className="bg-[rgba(20,20,30,0.6)] border border-[#00f5ff] text-[#e5e7eb] block w-full rounded-lg border-0 py-3 px-4 shadow-sm placeholder:text-[#9ca3af] focus:outline-none focus:ring-2 focus:ring-[#00f5ff] focus:border-transparent sm:text-sm sm:leading-6 shadow-[inset_0_0_5px_rgba(0,245,255,0.3)]"
                />
              </div>
            </div>
          ))}

          {(errorMessage || localError) && (
            <div className="text-[#ff2bd6] text-sm neon-glow">
              {errorMessage || localError}
            </div>
          )}

          <div>
            <button
              type="submit"
              disabled={isLoading}
              className="bg-[#ff2bd6] text-black flex w-full justify-center rounded-lg px-3 py-3.5 text-sm font-semibold leading-6 shadow-[0_0_15px_#ff2bd6] hover:shadow-[0_0_25px_#ff2bd6] transition-all duration-300 disabled:opacity-50"
            >
              {isLoading ? 'Loading...' : submitButtonText}
            </button>
          </div>
        </form>

        {onToggleForm && toggleText && (
          <p className="mt-6 text-center text-sm text-[#9ca3af] neon-glow">
            {toggleText}
            <button
              type="button"
              onClick={onToggleForm}
              className="font-semibold leading-6 text-[#00f5ff] hover:text-[#38bdf8] ml-1 transition-colors"
            >
              Click here
            </button>
          </p>
        )}
      </div>
    </div>
  );
}