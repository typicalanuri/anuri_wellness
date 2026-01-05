import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { HttpClient, HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-hero',
  imports: [FormsModule, MatFormFieldModule, MatInputModule, MatButtonModule, HttpClientModule],
  templateUrl: './hero.html',
  styleUrl: './hero.scss',
})

export class Hero {
  email: string = '';

  constructor(private http: HttpClient) {}

  submitEmail() {
    console.log(this.email);
    this.http.post('http://localhost:8000/subscribe', {email: this.email}, { headers: { 'Content-Type': 'application/json' } })
      .subscribe({
        next: () => alert('Subscribed!'),
        error: () => alert('Error!')
      });
  }
}
