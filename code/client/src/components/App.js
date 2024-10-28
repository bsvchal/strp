import React, { Suspense } from "react";
import { Router } from "@reach/router";

import Home from "../pages/Home";
import Signup from "../pages/Signup";
import Leaderboard from "../pages/Leaderboard";

const App = () => {
  return (
    <React.StrictMode>
      <Suspense fallback="loading">
        <Router>
          <Home path="/" />
          <Signup path="/signup" />
          <Leaderboard path="/leaderboard" />
        </Router>
      </Suspense>
    </React.StrictMode>
  );
};

export default App;
