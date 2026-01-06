'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/components/auth-provider';
import { Task, getTasks, createTask, updateTask, deleteTask, toggleTaskComplete } from '@/lib/api-client';
import { TaskForm } from '@/components/task-form';
import { TaskList } from '@/components/task-list';
import { Button } from '@/components/ui/button';

export default function DashboardPage() {
  const router = useRouter();
  const { user, logout } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!user) {
      router.push('/signin');
      return;
    }

    // Load tasks
    loadTasks();
  }, [user]);

  async function loadTasks() {
    if (!user) return;
    setLoading(true);
    try {
      const response = await getTasks(user.id);
      setTasks(response.tasks);
    } catch (error) {
      console.error('Failed to load tasks:', error);
    } finally {
      setLoading(false);
    }
  }

  async function handleCreateTask(title: string, description?: string) {
    try {
      const newTask: Task = await createTask(user.id, { title, description });
      setTasks([newTask, ...tasks]);
    } catch (error) {
      console.error('Failed to create task:', error);
      throw error;
    }
  }

  async function handleUpdateTask(taskId: string, title: string, description?: string) {
    try {
      const updatedTask: Task = await updateTask(user.id, taskId, { title, description });
      setTasks(tasks.map(t => t.id === taskId ? updatedTask : t));
    } catch (error) {
      console.error('Failed to update task:', error);
      throw error;
    }
  }

  async function handleDeleteTask(taskId: string) {
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
    try {
      const toggledTask: Task = await toggleTaskComplete(user.id, taskId);
      setTasks(tasks.map(t => t.id === taskId ? toggledTask : t));
    } catch (error) {
      console.error('Failed to toggle task:', error);
      throw error;
    }
  }

  if (!user) {
    return <div>Loading...</div>;
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
                  <span className="font-bold text-2xl">{tasks.length}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Completed</span>
                  <span className="font-bold text-2xl text-green-600">
                    {tasks.filter(t => t.completed).length}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Pending</span>
                  <span className="font-bold text-2xl text-amber-600">
                    {tasks.filter(t => !t.completed).length}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {loading ? (
          <div className="text-center py-8">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-r-2 border-primary"></div>
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
