import { AbstractControl, FormControl, ValidationErrors, ValidatorFn } from "@angular/forms";
import { Employee } from "../services/employee.model";


export function loginIDValidator(currentEmployees: any[]): ValidatorFn {
    let currentIDs: string[] = [];

    currentEmployees.forEach(
        (employee) => {
            currentIDs.push(employee.login_id);
            console.log('current emps');
        }
    );

    console.log(currentIDs);
    
    return (control: AbstractControl): ValidationErrors | null => {
        if (currentIDs.find(emp => emp == control.value)){
            return {'loginID': true }
        }
        return null;
    }
}