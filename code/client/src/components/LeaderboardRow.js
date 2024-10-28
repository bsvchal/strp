import React from "react";
import { getPriceDollars } from "../components/Util";

const LeaderboardRow = ({name, amount}) => {
  return (
    <div className="summary-row">
      <div className="summary-name">
        {name}
      </div>
      <div className="summary-sale">
        {getPriceDollars(amount, true)}
      </div>
    </div>
  );
};

export default LeaderboardRow;
