import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-thumbnails',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './thumbnails.html',
  styleUrl: './thumbnails.scss',
})
export class Thumbnails {
  items = [
    { image: '/assets/wellness_img_1.jpg', title: 'Wellness' },
    { image: '/assets/wellness_img_3.jpg', title: 'Positivity' },
    { image: '/assets/wellness_img_2.jpg', title: 'Game Changing' }
  ];
}
