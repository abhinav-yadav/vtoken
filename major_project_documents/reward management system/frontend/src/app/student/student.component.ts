import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { FormControl, FormGroup, FormBuilder, Validators } from '@angular/forms';

@Component({
    selector: 'app-student',
    templateUrl: './student.component.html',
    styleUrls: ['./student.component.css']
})
export class StudentComponent {

    studentData;
    studentName;
    studentBranch;
    passingYear;
    collegeID;
    degree;
    approved = false;
    succesfullSubmission = false;
    beforeSubmission = true;
    studentObj;
    alreadyConfirmed = false;

    studentForm = new FormGroup({
        studentEmail: new FormControl(),
        studentUniqueId: new FormControl()
    });

    constructor(private fb: FormBuilder, private httpClient: HttpClient) {
        this.createForm();
    }

    createForm() {
        this.studentForm = this.fb.group({
            studentEmail: ['', Validators.required],
            studentUniqueId: ['', Validators.required],
        });
    }

    submitDetails(event) {
        const target = event.target;
        const studentEmail = target.querySelector('#studentEmail').value;
        const studentUniqueId = target.querySelector('#studentUniqueId').value;
        this.succesfullSubmission = true;
        this.beforeSubmission = false;

        this.studentObj = { "email": studentEmail };

        this.httpClient.post(environment.getStudent, this.studentObj)
            .subscribe(
                response => {
                    console.log(response[0]);
                    console.log(response[0].SF);
                    if (response[0].SF == "0" || response[0].SF == "") {
                        this.studentData = response[0];
                        this.studentName = response[0].sname;
                        this.studentBranch = response[0].Sbranch;
                        this.passingYear = response[0].year;
                        this.degree = response[0].Degree;
                        this.collegeID = response[0].CollegeID;
                    } else {
                        this.alreadyConfirmed = true;
                    }
                },
                err => {
                    console.log("Error Ocurred" + err);
                }
            )
    }

    approve() {
        const studentObj = { "ID": this.studentData.ID, "sf": "1", "email": this.studentData.Email }
        console.log(studentObj);
        this.httpClient.post(environment.verifyStudent, studentObj)
            .subscribe(
                response => {
                    console.log(response);
                    this.approved = true;
                    this.studentForm.reset();
                },
                err => {
                    console.log("Error Ocurred" + err);
                }
            )
    }
}