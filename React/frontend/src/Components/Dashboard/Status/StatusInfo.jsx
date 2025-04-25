const Statusinfomoney = (props) => {
  return (
    <div className="statusinfo-container">
      <p>{props.name}</p>
      <div>
        <h3>Rs. {props.amount}</h3>
      </div>
    </div>
  );
};

const Statusinfopercent = (props) => {
  return (
    <div className="statusinfo-container">
      <p>{props.name}</p>
      <div>
        <h3> {props.growth}</h3>
      </div>
    </div>
  );
};

export { Statusinfomoney, Statusinfopercent };
