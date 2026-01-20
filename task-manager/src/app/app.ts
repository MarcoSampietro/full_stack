import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

interface Task {
  id: number;
  title: string;
  completed: boolean;
}

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './app.html',
  styleUrls: ['./app.css']
})
export class App implements OnInit {
  tasks: Task[] = [];
  newTaskTitle: string = '';

  // !!! RIMETTI QUI IL TUO URL DI CODESPACES (senza slash finale) !!!
  private apiUrl = 'https://fluffy-space-capybara-v6pjp475j964fp957-5000.app.github.dev/tasks';

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.getTasks();
  }

  getTasks() {
    this.http.get<Task[]>(this.apiUrl).subscribe(data => {
      this.tasks = data;
    });
  }

  addTask() {
    if (!this.newTaskTitle.trim()) return;

    const body = { title: this.newTaskTitle };
    this.http.post<Task>(this.apiUrl, body).subscribe(newTask => {
      this.tasks.push(newTask);
      this.newTaskTitle = '';
    });
  }

  deleteTask(id: number) {
    this.tasks = this.tasks.filter(t => t.id !== id);
    this.http.delete(`${this.apiUrl}/${id}`).subscribe();
  }

  // FUNZIONE NUOVA: Gestisce il click sulla checkbox
  toggleTask(task: Task) {
    // 1. Invertiamo lo stato visivamente (subito)
    task.completed = !task.completed;

    // 2. Aggiorniamo il database
    this.http.put(`${this.apiUrl}/${task.id}`, { completed: task.completed }).subscribe({
      error: (err) => {
        console.error("Errore aggiornamento", err);
        // Se fallisce, rimettiamo com'era prima
        task.completed = !task.completed;
      }
    });
  }
}