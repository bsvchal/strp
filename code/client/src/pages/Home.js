import React from "react";
import { Link } from "@reach/router";
import Header from "../components/Header";

//Show home page
const Home = () => {
  return (
    <main className="main-global">
      <Header subheader = "Merch Challenge"/>
      
      <div className="home-body">
        Want to win free tickets to see the Afrobeatles at their next concert? Sign up below to become a seller in the Merch Challenge!
      </div>
      <div className="button-list">
        <Link to="/signup">
        <button id="signup">Become a Seller</button>
      </Link>
      <Link to="/leaderboard">
        <button id="leaderboard">View Leaderboard</button>
      </Link>
      </div>
    </main>
  );
};

export default Home;
