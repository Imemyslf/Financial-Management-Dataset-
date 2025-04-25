export default Statusinfo = (props) => {
    return (
        <div>
            <p>{props.name}</p>
            <div>
                <h3>Rs.</h3>
                <h3>{props.amount}</h3>   
            </div>
        </div>
    )
}