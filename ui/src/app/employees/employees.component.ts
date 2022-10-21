import { Component, OnDestroy, OnInit, TemplateRef } from "@angular/core";
import { Subscription } from "rxjs";
import { DBApiService } from "../services/db-api.service";
import { Employee } from "../services/employee.model";
import { Router } from '@angular/router';
import { BsModalService, BsModalRef } from 'ngx-bootstrap/modal';




@Component({
    selector: 'app-employees',
    templateUrl: './employees.component.html',
    styleUrls: ['./employees.component.css']
})
export class EmployeesComponent implements OnInit, OnDestroy {
    title = 'Onboarded Employees'

    ModalRef: BsModalRef | undefined;
    deleteMessage: string = "";

    employeesListSubs: Subscription = new Subscription;
    allEmployees: Employee[] = [];
    employeesList: Employee[] = [];

    selectedEmployee!: Employee;
    selectedDate: string = '';

    constructor(public DB: DBApiService, private router: Router, private modalService: BsModalService) {}

    ngOnInit(): void {
        this.employeesListSubs = this.DB.getEmployees().subscribe(
            data => {
                this.allEmployees = data;
                this.employeesList = data;
            }
        );
        
    }

    filterEmployees(): void {
        console.log(`Date: ${this.selectedDate}`);
        if (this.selectedDate === '') {
            this.employeesList = this.allEmployees;
            return;
        }
        this.employeesListSubs = this.DB.getEmployeesDate(this.selectedDate).subscribe(
            data => {
                this.employeesList = data;
            }
        );
    }

    viewEmployee(selectedEmployee: Employee): void {
        console.log("Viewing an employee:");
        console.log(selectedEmployee);
        // save data in selectedEmployee
        // navigate to employee view page
        // populate page with data saved from selectedEmployee

        /*
        this.employeesListSubs = this.DB.getEmployees().subscribe(
            data => {
                this.employeesList = data;
            }
        );
        */
    }

    editEmployee(selectedEmployee: Employee, template: TemplateRef<any>): void {
        console.log("Editing an employee:");
        this.ModalRef = this.modalService.show(template, {class: 'modal-sm'});
        console.log(selectedEmployee);
        // use selectedEmployee.login_id to make a call to the api
        // open Modal - ChildComponent
        // collect data
        // make call to API to edit employee
    }

    deleteEmployee(selectedEmployee: Employee, template: TemplateRef<any>): void {
        this.selectedEmployee = selectedEmployee;
        this.ModalRef = this.modalService.show(template, {class: 'modal-sm'});
        console.log("Deleting an employee:");
        console.log(selectedEmployee);
        // use selectedEmployee.login_id to make a call to the api
        // open Modal - ChildComponent
        // are you sure you want to delete Employee X
        // if end user clicks yes, delete employee - make a call to the api
    }

    confirmDelete(): void {
        console.log(`Deleting user ${this.selectedEmployee?.login_id}`);
        this.deleteMessage = `${this.selectedEmployee?.name} has been deleted. The User ${this.selectedEmployee?.login_id} has been deactivated.`;
        this.ModalRef?.hide();

        this.employeesListSubs = this.DB.deleteEmployee(this.selectedEmployee?.login_id).subscribe(
            data => {
                console.log(data);
            }
        )
    }

    cancelDelete(): void {
        console.log("Cancel delete");
        this.ModalRef?.hide();
    }


    newEmployee(){
        console.log("New Employee");
        this.router.navigateByUrl('/add-employee');
    }


    ngOnDestroy(): void {
        this.employeesListSubs.unsubscribe();
    }
}