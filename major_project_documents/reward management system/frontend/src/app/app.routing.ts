import { RouterModule, Routes } from '@angular/router';

import { DepartmentComponent } from './department/department.component';
import { StudentComponent } from './student/student.component';
import { UniversityComponent } from './university/university.component';
import { ValidateComponent } from './validate/validate.component';
import { HomeComponent } from './home/home.component';
import { AddStudent } from './addStudent/addStudent.component';

export const appRoutes: Routes = [

    { path: '', component: HomeComponent, pathMatch: "full" },
    { path: 'university', component: UniversityComponent, pathMatch: "full" },
    { path: 'college', component: DepartmentComponent },
    { path: 'student', component: StudentComponent },
    { path: 'validate', component: ValidateComponent },
    { path: 'addstudent', component: AddStudent },

];

export const routing = RouterModule.forRoot(appRoutes);