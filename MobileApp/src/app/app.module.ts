import { BrowserModule } from '@angular/platform-browser';
import { ErrorHandler, NgModule } from '@angular/core';
import { IonicApp, IonicErrorHandler, IonicModule } from 'ionic-angular';

import { MyApp } from './app.component';
import { HttpModule} from '@angular/http';
import { LoginPage } from '../pages/login/login';
import { RegisterPage } from '../pages/register/register';
import { UserDetailsPage } from '../pages/user-details/user-details';
import { OrganizationDetailsPage } from '../pages/organization-details/organization-details';
import { EventsPage } from '../pages/events/events';
import { CreateEventPage } from '../pages/create-event/create-event';
import { EventManagementPage } from '../pages/event-management/event-management';
import { EventsDashBoardPage } from '../pages/events-dash-board/events-dash-board';
import { EventDetailsViewPage } from '../pages/event-details-view/event-details-view';
import { UserPublicProfilePage } from '../pages/user-public-profile/user-public-profile';
import { UserApplicationViewPage } from '../pages/user-application-view/user-application-view';
import { OrganizationProfileEditPage } from '../pages/organization-profile-edit/organization-profile-edit';
import { UserProfileEditPage } from '../pages/user-profile-edit/user-profile-edit';
import { FeedbackFormPage } from '../pages/feedback-form/feedback-form';

import { Base64 } from '@ionic-native/base64';

import { SplashScreen } from '@ionic-native/splash-screen';
import { LoginProvider } from '../providers/login/login';
import { StatusBar } from '@ionic-native/status-bar';
import { RequestProvider } from '../providers/request/request';
import { RegisterProvider } from '../providers/register/register';
import { RegisterCompanyProvider } from '../providers/register-company/register-company';
import { EventsProvider } from '../providers/events/events';
import { EventOrganizationDescriptionPage } from '../pages/event-organization-description/event-organization-description';
import { EventParticipantsPage } from '../pages/event-participants/event-participants';
import { UserApplicationProvider } from '../providers/user-application/user-application';
import { FileChooser } from '@ionic-native/file-chooser';
import { FileProvider } from '../providers/file/file';
import { FeedbackProvider } from '../providers/feedback/feedback';
import { StarRatingModule } from 'ionic3-star-rating';


@NgModule({
  declarations: [
    MyApp,
    LoginPage,
    RegisterPage,
    UserDetailsPage,
    OrganizationDetailsPage,
    EventsPage,
    CreateEventPage,
    EventManagementPage,
    EventsDashBoardPage,
    EventOrganizationDescriptionPage,
    EventParticipantsPage,
    EventDetailsViewPage,
    UserPublicProfilePage,
    UserApplicationViewPage,
    OrganizationProfileEditPage,
    UserProfileEditPage,
    FeedbackFormPage
  ],
  imports: [
    BrowserModule,
    HttpModule,
    StarRatingModule,
    IonicModule.forRoot(MyApp, { scrollAssist: false, autoFocusAssist: false }),
  ],
  bootstrap: [IonicApp],
  entryComponents: [
    MyApp,
    LoginPage, 
    RegisterPage,
    LoginPage,
    UserDetailsPage,
    OrganizationDetailsPage,
    EventsPage,
    CreateEventPage,
    EventManagementPage,
    EventsDashBoardPage,
    EventOrganizationDescriptionPage,
    EventParticipantsPage,
    EventDetailsViewPage,
    UserPublicProfilePage,
    UserApplicationViewPage,
    OrganizationProfileEditPage,
    UserProfileEditPage,
    FeedbackFormPage
  ],
  providers: [
    StatusBar,
    SplashScreen,
    {provide: ErrorHandler, useClass: IonicErrorHandler},
    LoginProvider,
    RequestProvider,
    EventsProvider,
    RegisterProvider,
    RegisterCompanyProvider,
    UserApplicationProvider,
    Base64,
    FileChooser,
    FileProvider,
    FeedbackProvider
  ]
})
export class AppModule {}
