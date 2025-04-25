import {Statusinfomoney, Statusinfopercent} from "./Status/StatusInfo";
import "../../style/Dashboard/Statusbar/statusbar.css";

const Statusbar = () => {
  return (
    <>
    <div className="statusbar-container">
      <Statusinfomoney name="Net Revenue" amount="1450600" />
      <Statusinfopercent name="Quarter Growth" growth="33%" />
      <Statusinfomoney name="ARR" amount="1450600" />
    </div>
    </>
  );
};

export default Statusbar;