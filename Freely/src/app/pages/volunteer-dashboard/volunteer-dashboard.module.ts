import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Routes, RouterModule } from '@angular/router';

import { IonicModule } from '@ionic/angular';

import { VolunteerDashboardPage } from './volunteer-dashboard.page';

const routes: Routes = [
  {
    path: '',
    component: VolunteerDashboardPage
  }
];

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    RouterModule.forChild(routes)
  ],
  declarations: [VolunteerDashboardPage]
})
export class VolunteerDashboardPageModule {}
