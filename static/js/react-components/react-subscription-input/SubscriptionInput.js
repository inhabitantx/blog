import React from 'react'
import RenderDom from 'react-dom'


// Usage: <SubscriptionInput
//   containerClassName="subscription-popup"
//   canBeClosed="true"
//   heading="Subscribe!"
//   headingClass="subscription-popup-heading"
//   subheading="Enter your mailaddress to receive updates about my trips"
//   subheadingClass="subscription-popup-subheading"
//   formClass="popup-form"
//   inputClass="form-control"
//   buttonClass="btn btn-dark footer-button"
// />

export default class SubscriptionInput extends React.Component {
  constructor(props){
    super(props)

    this.state = {
      email: '',
      submitted: false,
      showForm: this.props.showForm
    }
  }

    handleValueChange = (event) => {
      this.setState({
        email: event.target.value,
      })
    }

    handleSubmit = (event) => {
      event.preventDefault()
      this.submitForm(this.state.email)
    }

    submitForm = async (email) => {
      try{
        const response = await fetch('/addsubscriber', {
          method: 'POST',
          headers: {'content-type': 'application/json'},
          body: JSON.stringify({email}),
        })
        const {message, status} = await response.json()
          this.setState({
            message,
            submitted: true,
            status,
          })
      }catch(err){
        this.setState({
          message: err,
        })
      }
    }


    render(){

      {if(!this.state.submitted && this.state.showForm){
        return(
          <div
            styles={{opacity:this.props.opacity}}
            className={this.props.containerClassName}>
            {this.props.heading && (
              <h2
                className={this.props.headingClass}
              >
              {this.props.heading}
              </h2>

            )}
            {this.props.subheading && (
              <h3
                className={this.props.subheadingClass}
              >
              {this.props.subheading}
              </h3>
            )}
            <form
              className={this.props.formClass}
            >
              <input
                className={this.props.inputClass}
                value={this.state.email}
                onChange={this.handleValueChange}
                placeholder="Enter your mail-address"
              />
              <button
                className={this.props.buttonClass}
                onClick={this.handleSubmit}
              >Submit</button>
            </form>
          </div>
        )
      }else if(this.state.submitted && this.state.showForm){
          if(this.state.status === "ok"){
            return(
              <div style={{paddingTop: "2em"}}>
                {this.props.canBeClosed &&(
                  <div
                    className="close-popup">
                    <i
                      className="fa fa-close close-popup"
                      onClick={this.props.close}
                    ></i>
                  </div>
                )}
                <h2
                  className="subscription-successful"
                >
                  <i className="fa fa-check"></i>
                  {this.state.message}
                </h2>
              </div>
            )
          }else{
            return(
              <div style={{paddingTop: "2em"}}>
                {this.props.canBeClosed &&(

                  <div
                    className="close-popup">
                    <i
                      className="fa fa-close close-popup"
                      onClick={this.props.close}
                    ></i>
                  </div>
                )}
                <h2
                  className="subscription-unsuccessful"
                >
                  <i className="fa fa-close"></i>

                  {this.state.message}
                </h2>
              </div>
            )

          }
      }else{
        return null
      }}
    }
}
