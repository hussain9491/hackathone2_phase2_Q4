'use client';

import { Task } from '@/lib/api-client';
import { Button } from '@/components/ui/button';

export interface TaskItemProps {
  task: Task;
  onUpdate: (taskId: string, title: string, description?: string) => void;
  onDelete: (taskId: string) => void;
  onToggle: (taskId: string) => void;
}

export function TaskItem({ task, onUpdate, onDelete, onToggle }: TaskItemProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(task.title);
  const [editDescription, setEditDescription] = useState(task.description || '');
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

  const handleSave = () => {
    onUpdate(task.id, editTitle, editDescription || undefined);
    setIsEditing(false);
  };

  const handleToggle = () => {
    onToggle(task.id);
  };

  return (
    <div className={`bg-card text-card-foreground rounded-lg border shadow-sm p-4 mb-3 ${task.completed ? 'opacity-60' : ''}`}>
      <div className="flex items-start gap-3">
        <input
          type="checkbox"
          checked={task.completed}
          onChange={handleToggle}
          className="mt-1 min-h-[20px] min-w-[20px]"
          disabled={isEditing}
        />

        <div className="flex-1 space-y-2">
          {isEditing ? (
            <>
              <input
                type="text"
                value={editTitle}
                onChange={(e) => setEditTitle(e.target.value)}
                maxLength={200}
                className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
              />
              <textarea
                value={editDescription}
                onChange={(e) => setEditDescription(e.target.value)}
                maxLength={1000}
                rows={2}
                className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring mt-2"
              />
            </>
          ) : (
            <>
              <h3 className={`font-semibold text-lg ${task.completed ? 'line-through text-muted-foreground' : ''}`}>
                {task.title}
              </h3>
              {task.description && (
                <p className={`text-sm ${task.completed ? 'line-through text-muted-foreground' : 'text-muted-foreground'}`}>
                  {task.description}
                </p>
              )}
            </>
          )}
        </div>

        <div className="flex gap-2">
          {isEditing ? (
            <div className="flex gap-2">
              <Button onClick={handleSave} size="sm" variant="default">
                Save
              </Button>
              <Button onClick={() => setIsEditing(false)} size="sm" variant="outline">
                Cancel
              </Button>
            </div>
          ) : (
            <div className="flex gap-2">
              <Button onClick={() => setIsEditing(true)} size="sm" variant="outline">
                Edit
              </Button>
              <Button
                onClick={() => setShowDeleteConfirm(true)}
                size="sm"
                variant="destructive"
                disabled={showDeleteConfirm}
              >
                Delete
              </Button>
            </div>
          )}

          {showDeleteConfirm && (
            <div className="flex gap-2">
              <Button
                onClick={() => onDelete(task.id)}
                size="sm"
                variant="destructive"
              >
                Confirm
              </Button>
              <Button
                onClick={() => setShowDeleteConfirm(false)}
                size="sm"
                variant="outline"
              >
                Cancel
              </Button>
            </div>
          )}
        </div>
      </div>

      <div className="text-xs text-muted-foreground mt-2">
        Created: {new Date(task.created_at).toLocaleDateString()} |
        Updated: {new Date(task.updated_at).toLocaleDateString()}
      </div>
    </div>
  );
}
