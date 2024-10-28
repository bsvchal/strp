import React from "react";
import { Link } from "@reach/router";
const Header = ({ subheader }) => {
  return (
    <div className="header">
      <div className="banner">
        <span className="banner-stripe banner-red"></span>
        <span className="banner-stripe banner-yellow"></span>
        <span className="banner-stripe banner-green"></span>
      </div>
      <div className="title"><Link to="/">The Afrobeatles</Link></div>
      <div className="subheader">{subheader}</div>
    </div>
  );
};

export default Header;
