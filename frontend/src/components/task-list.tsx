'use client';

import { Task } from '@/lib/api-client';
import { TaskItem } from './task-item';

export interface TaskListProps {
  tasks: Task[];
  onUpdate: (taskId: string, title: string, description?: string) => void;
  onDelete: (taskId: string) => void;
  onToggle: (taskId: string) => void;
}

export function TaskList({ tasks, onUpdate, onDelete, onToggle }: TaskListProps) {
  // Sort by completed (pending first) then created_at DESC
  const sortedTasks = [...tasks].sort((a, b) => {
    if (a.completed === b.completed) {
      const dateA = a.created_at ? new Date(a.created_at).getTime() : 0;
      const dateB = b.created_at ? new Date(b.created_at).getTime() : 0;
      return dateB - dateA;
    }
    return a.completed ? 1 : -1;
  });

  if (tasks.length === 0) {
    return (
      <div className="bg-card text-card-foreground rounded-lg border shadow-sm p-8 text-center">
        <h3 className="text-lg font-semibold mb-2">No tasks yet</h3>
        <p className="text-sm text-muted-foreground">
          Create your first task to get started
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {sortedTasks.map((task) => (
        <TaskItem
          key={task.id}
          task={task}
          onUpdate={onUpdate}
          onDelete={onDelete}
          onToggle={onToggle}
        />
      ))}
    </div>
  );
}
