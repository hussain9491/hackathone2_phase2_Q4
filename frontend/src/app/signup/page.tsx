'use client';

import { SignupForm } from '@/components/signup-form';

export default function SignupPage() {
  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto py-8">
        <SignupForm />
      </div>
    </div>
  );
}
