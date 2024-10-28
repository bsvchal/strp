import React, { useEffect } from "react";
import Header from "../components/Header";
import RegistrationForm from "../components/RegistrationForm";
const Signup = () => {
  useEffect(() => {
    const setup = async () => {
      
    };
    setup();
  }, []);

  return (
    <main className="main-global">
      <Header subheader={"Become a Seller"}/>
      {
        //Component to process user info for registration.
      }
      <RegistrationForm />
     
    </main>
  );
};

export default Signup;
