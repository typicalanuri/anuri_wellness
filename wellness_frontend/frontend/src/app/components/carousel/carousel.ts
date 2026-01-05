import { Component } from '@angular/core';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-carousel',
  standalone: true,
  imports: [NgbModule, CommonModule],
  templateUrl: './carousel.html',
  styleUrl: './carousel.scss',
})
export class Carousel {
  slides = [
    { image: 'https://via.placeholder.com/800x400', title: 'Slide 1', description: 'Description 1' },
    { image: 'https://via.placeholder.com/800x400', title: 'Slide 2', description: 'Description 2' },
    { image: 'https://via.placeholder.com/800x400', title: 'Slide 3', description: 'Description 3' }
  ];
}
