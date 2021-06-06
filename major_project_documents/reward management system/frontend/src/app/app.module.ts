import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { routing } from './app.routing';

import { AppComponent } from './app.component';
import { HttpClientModule } from '@angular/common/http';
import { ReactiveFormsModule } from '@angular/forms';

import { DepartmentComponent } from './department/department.component';
import { StudentComponent } from './student/student.component';
import { UniversityComponent } from './university/university.component';
import { ValidateComponent } from './validate/validate.component';
import { HomeComponent } from './home/home.component';
import { AddStudent } from './addStudent/addStudent.component';



@NgModule({
  declarations: [
    AppComponent,
    DepartmentComponent,
    StudentComponent,
    UniversityComponent,
    ValidateComponent,
    HomeComponent,
    AddStudent
  ],
  imports: [
    BrowserModule,

    HttpClientModule,

    ReactiveFormsModule,
    RouterModule,
    routing
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
