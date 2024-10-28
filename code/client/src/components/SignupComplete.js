import React, { useEffect } from "react";

const SignupComplete = ({ active, paymentLink }) => {
  useEffect(() => {
  }, []);

  const copyToClipboard = async () => {
    navigator.clipboard.writeText(paymentLink);
  };

  if (active) {
    return (
      <div className="signup-complete">
          Copy your personal link below to share on your socials.
          <div className="payment-link-section">
          <span className="payment-link" id="payment-link">
              {paymentLink}
              </span>
              <span className="copy-button">
              <img id ="copy-button" src="/assets/img/copyicon.png" alt="Copy Payment Link" className="copy-img" onClick={copyToClipboard}/>
              </span>
          </div>
      </div>
    );
  } else {
    return "";
  }
};

export default SignupComplete;
