import "../../style/Dashboard/Userbar/userbar.css"
import userImage from "../../assets/Images/UserProfile.png"
const Userbar = () => {
  return (
    <div className="userbar-container">
      <div className="userbar">
        <img src={userImage} alt="User-image"/>
      </div>
    </div>
  );
};

export default Userbar