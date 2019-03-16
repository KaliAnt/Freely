import { Component, OnInit } from '@angular/core';
import { RouterModule, Routes, Navigation } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss'],
})

export class LoginPage implements OnInit {
  loginProvider: any;
  ngOnInit(): void {
    throw new Error("Method not implemented.");
  }

  private account: any = {
    email: "",
    password: ""
  };
  private rememberPass: boolean = false;
  private isLoading: boolean = false;

  constructor() { }

  ionViewDidLoad() {
   
    if(localStorage.getItem("rememberPass")=="true"){
    
      this.rememberPass=true;
    }else{
      this.rememberPass=false;
    }

    if(this.rememberPass){
      this.account.email=localStorage.getItem("email");
      this.account.password=localStorage.getItem("password");
    }
  }

  doLogin(){
    this.loginProvider.login(this.account.email, this.account.password).then(result =>{
      console.log(result);
      if(result.status == "OK"){
        sessionStorage.setItem("type", result.type);
        if(result.type == "volunteer"){
          sessionStorage.setItem("firstName", result.data.firstName);
        }else{
          sessionStorage.setItem("name", result.data.name);
        }
        //if(sessionStorage.getItem("type") == "volunteer"){
          //this.navCtrl.setRoot(UserDetailsPage);
        //}else{
          //this.navCtrl.setRoot(OrganizationDetailsPage);
        //}
        
      //}else{
        //this.displayErrorAlert("Invalid login data!");
      }
    });

    localStorage.setItem("rememberPass",this.rememberPass.toString()); 
    if(this.rememberPass){
      localStorage.setItem("email",this.account.email);
      localStorage.setItem("password",this.account.password);
      
    }
  }

  passIcon() {
    if (this.rememberPass) {
      return "checkbox";
    }
    return "square";
  }

  togglePass() {
    this.rememberPass =! this.rememberPass;
  }

}
