'use client';

import { SigninForm } from '@/components/signin-form';

export default function SigninPage() {
  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto py-8">
        <SigninForm />
      </div>
    </div>
  );
}
