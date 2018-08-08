



ReactDOM.render(
  <SubscriptionInput
    containerClassName="subscription-popup"
    canBeClosed="true"
    heading="Subscribe!"
    headingClass="subscription-popup-heading"
    subheading="Enter your mailaddress to receive updates about my trips"
    subheadingClass="subscription-popup-subheading"
    formClass="popup-form"
    inputClass="form-control"
    buttonClass="btn btn-dark footer-button"
  />,
  document.getElementById('subscription-popup')
)
ReactDOM.render(
  <SubscriptionInput
      containerClassName="footer-subscription"
      formClass="footer-form"
      inputClass="form-control"
      buttonClass="btn btn-dark footer-button"
  />,
  document.getElementById('footer-subscription')
)
