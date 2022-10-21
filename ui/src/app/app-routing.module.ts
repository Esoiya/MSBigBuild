import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AddDepartmentComponent } from './add-department/add-department.component';
import { AddEmployeeComponent } from './add-employee/add-employee.component';
import { DepartmentsComponent } from './departments/departments.component';
import { EmployeesComponent } from './employees/employees.component';
import { ViewEmployeeComponent } from './view-employee/view-employee.component';

const routes: Routes = [
  { path: 'departments', component: DepartmentsComponent},
  { path: 'employees', component: EmployeesComponent},
  { path: 'add-employee', component: AddEmployeeComponent},
  { path: 'add-department', component: AddDepartmentComponent},
  { path: 'view-employee', component: ViewEmployeeComponent}

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
