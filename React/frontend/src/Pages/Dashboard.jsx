import CompanyBar from "../Components/Dashboard/CompanyBar";
import Heatmap from "../Components/Dashboard/Heatmap";
import Sankey from "../Components/Dashboard/Sankey";
import StatusBar from "../Components/Dashboard/StatusBar";
import UserBar from "../Components/Dashboard/UserBar";

export default Dashboard = () => {
  return (
    <>
      <UserBar />
      <CompanyBar companyName="ANITISOCIAL Pvt Ltd. " />
      <StatusBar />
      <Heatmap />
      <Sankey />
    </>
  );
};
