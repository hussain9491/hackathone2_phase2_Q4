  'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/components/auth-provider';
import { Task, getTasks, createTask, updateTask, deleteTask, toggleTaskComplete } from '@/lib/api-client';
import { TaskForm } from '@/components/task-form';
import { TaskList } from '@/components/task-list';
import { Button } from '@/components/ui/button';
import { Loading } from '@/components/ui/loading';

export default function DashboardPage() {
  const router = useRouter();
  const { user, logout, loading: authLoading } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [pageLoading, setPageLoading] = useState(true);

  useEffect(() => {
    // Only redirect if auth is loaded and user is not authenticated
    if (!authLoading) {
      if (!user) {
        router.replace('/signin');
      } else {
        // Load tasks if user is authenticated
        loadTasks();
      }
    }
  }, [user, authLoading]);

  async function loadTasks() {
    if (!user) return;
    setPageLoading(true);
    try {
      const response = await getTasks(user.id);
      setTasks(response.tasks);
    } catch (error) {
      console.error('Failed to load tasks:', error);
    } finally {
      setPageLoading(false);
    }
  }

  async function handleCreateTask(title: string, description?: string) {
    if (!user) return;
    try {
      const newTask: Task = await createTask(user.id, { title, description });
      setTasks([newTask, ...tasks]);
    } catch (error) {
      console.error('Failed to create task:', error);
      throw error;
    }
  }

  async function handleUpdateTask(taskId: string, title: string, description?: string) {
    if (!user) return;
    try {
      const updatedTask: Task = await updateTask(user.id, taskId, { title, description });
      setTasks(tasks.map(t => t.id === taskId ? updatedTask : t));
    } catch (error) {
      console.error('Failed to update task:', error);
      throw error;
    }
  }

  async function handleDeleteTask(taskId: string) {
    if (!user) return;
    if (!confirm('Are you sure you want to delete this task?')) return;

    try {
      await deleteTask(user.id, taskId);
      setTasks(tasks.filter(t => t.id !== taskId));
    } catch (error) {
      console.error('Failed to delete task:', error);
      throw error;
    }
  }

  async function handleToggleTask(taskId: string) {
    if (!user) return;
    try {
      const toggledTask: Task = await toggleTaskComplete(user.id, taskId);
      setTasks(tasks.map(t => t.id === taskId ? toggledTask : t));
    } catch (error) {
      console.error('Failed to toggle task:', error);
      throw error;
    }
  }

  // Show loading state while auth state is being determined
  if (authLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <Loading text="Checking authentication..." />
      </div>
    );
  }

  // If user is not authenticated, we should have been redirected, but just in case:
  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <Loading text="Redirecting to sign in..." />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b">
        <div className="container mx-auto py-4 px-4 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold">My Tasks</h1>
            <p className="text-sm text-muted-foreground">
              {user.email}
            </p>
          </div>
          <Button onClick={logout} variant="outline">
            Sign Out
          </Button>
        </div>
      </header>

      <main className="container mx-auto py-8 px-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="md:col-span-2">
            <TaskForm onSubmit={handleCreateTask} />
          </div>
          <div className="md:col-span-1">
            <div className="bg-card text-card-foreground rounded-lg border p-6">
              <h2 className="text-xl font-semibold mb-4">Quick Stats</h2>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Total Tasks</span>
                  <span className="font-bold text-2xl">{tasks?.length ?? 0}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Completed</span>
                  <span className="font-bold text-2xl text-green-600">
                    {tasks?.filter(t => t.completed)?.length ?? 0}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Pending</span>
                  <span className="font-bold text-2xl text-amber-600">
                    {tasks?.filter(t => !t.completed)?.length ?? 0}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {pageLoading ? (
          <div className="text-center py-8">
            <Loading />
          </div>
        ) : (
          <TaskList
            tasks={tasks}
            onUpdate={handleUpdateTask}
            onDelete={handleDeleteTask}
            onToggle={handleToggleTask}
          />
        )}
      </main>
    </div>
  );
}
