import { Component, OnDestroy, OnInit } from "@angular/core";
import { Subscription } from "rxjs";
import { DBApiService } from "../services/db-api.service";
import { Employee } from "../services/employee.model";
import { Router } from '@angular/router';
import { Location } from "@angular/common";
import { FormControl, FormGroup, Validators } from "@angular/forms";
import { Department } from "../services/department.model";
import { loginIDValidator } from './add-employee-validator';





@Component({
    selector: 'app-add-employee',
    templateUrl: './add-employee.component.html',
    styleUrls: ['./add-employee.component.css']
})
export class AddEmployeeComponent implements OnInit, OnDestroy {
    title = 'Add New Employee'

    newEmployeeSubs: Subscription = new Subscription;

    newEmployee!: Employee;

    allDepartments: Department[] = [];

    currentEmployees: Employee[] = [];

    selectDepartmentID: string = '';

    employeeForm! : FormGroup;

    constructor(public DB: DBApiService, private router: Router, private location: Location) {}

    ngOnInit(): void {
        this.newEmployeeSubs = this.DB.getDepartments().subscribe(
            data => {
                this.allDepartments = data;
            }
        );

        /*
        this.newEmployeeSubs = this.DB.getEmployees().subscribe(
            data => {
                this.currentEmployees = data;
            }
        );
        */

        this.employeeForm = new FormGroup({
            login_id: new FormControl(
                '',
                [
                    Validators.required,
                    Validators.maxLength(10),
                    //loginIDValidator(this.currentEmployees)
                ]),
            dept_id: new FormControl(
                '',
                [
                    Validators.required
                ]
            ),
            name: new FormControl(
                '',
                [
                    Validators.required
                ]
            ),
            onboarded: new FormControl(
                '',
                [Validators.required]
            )
            
        })
        
    }

    get login_id() {
        return this.employeeForm.get('login_id')!;
    }

    get dept_id() {
        return this.employeeForm.get('dept_id')!;
    }

    get name() {
        return this.employeeForm.get('name')!;
    }

    get onboarded(){
        return this.employeeForm.get('onboarded')!;
    }

    addEmployee(): void {
        this.newEmployee = new Employee(
            this.employeeForm.value.login_id,
            this.employeeForm.value.dept_id,
            this.employeeForm.value.name,
            this.employeeForm.value.onboarded
        );
        console.log(this.newEmployee);
        
        this.newEmployeeSubs = this.DB.addEmployee(this.newEmployee).subscribe(
            status => console.log(status)
        );

    }


    viewAllEmployees(): void {
        console.log("Back to Onboarded Employees");
        this.router.navigateByUrl('/employees');
    }

    ngOnDestroy(): void {
        this.newEmployeeSubs.unsubscribe();
        
    }
}