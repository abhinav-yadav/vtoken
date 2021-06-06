import { Component, OnInit, ElementRef, Input } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormControl, FormGroup, FormBuilder, Validators } from '@angular/forms';
import { environment } from '../../environments/environment';

import "rxjs/add/operator/do";
import "rxjs/add/operator/map";

@Component({
    selector: 'app-validate',
    templateUrl: './validate.component.html',
    styleUrls: ['./validate.component.css']
})
export class ValidateComponent {

    doc;
    flag = false;
    link;
    fla = false;

    //Create Form Group
    form = new FormGroup({
    });

    constructor(private fb: FormBuilder, private httpClient: HttpClient, private el: ElementRef) { }

    validate(event) {
        const target = event.target;
        const validate = target.querySelector('#validate').value;

        //locate the file element meant for the file upload.
        const inputEl: HTMLInputElement = this.el.nativeElement.querySelector('#fileToUpload');
        const fileCount: number = inputEl.files.length;
        const formData = new FormData();

        //check if the filecount is greater than zero, to be sure a file was selected.
        if (fileCount > 0) {

            formData.append('transaction_id', validate);
            formData.append('file-to-upload', inputEl.files.item(0));

            console.log(formData);
            
            this.httpClient.post(environment.validate, formData)
                .subscribe(
                    (response) => {
                        console.log(response);
                        this.fla = false;
                        this.link = 'https://rinkeby.etherscan.io/tx/'+response[0].id;
                        if (response[0].status === '1') {
                            this.fla = true;
                            this.doc = 'Your Document is Valid  For more Details '  
                        } else {
                            this.doc = 'Your Document is not Valid '
                        }
                        this.flag = true;
                       // this.fla = false;
                    },
                    err => {
                        console.log("Error Ocurred" + err);
                    }
                )
        }
    }
}