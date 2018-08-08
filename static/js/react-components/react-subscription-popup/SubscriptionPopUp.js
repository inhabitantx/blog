import React from 'react'
import ReactDOM from 'react-dom'

import SubscriptionInput from '../react-subscription-input/SubscriptionInput'

//Changing its opacity while scrolling on the y axis. Bottom most visible.

const TRIGGER = 800

const debounce = (func, wait) => {
  let timeout
  return (...args) => {
    clearTimeout(timeout)
    timeout = setTimeout(() => func.apply(this, args), wait)
  }
}

export default class SubscriptionPopUp extends React.Component{
  state = {
    submitted: false,
    visibility: false,
    display: "block",
    opacity: 0,
    scrollPositionY: 0,
  }

  componentDidMount() {
  //Add eventlistener for scrolling event
    return window.addEventListener('scroll', debounce(this.handleScroll, 16))
  }

  componentWillUnmount() {
    return window.removeEventListener('scroll', debounce(this.handleScroll, 16))
  }

  handleScroll = () => {
    // + is unary operator, same as Number(window.scrollY)
    const scrollPositionY = +window.scrollY
    if(scrollPositionY > TRIGGER){
      var visibility = true
    }else{
      var visibility = false
    }
    while(visibility && this.state.opacity < 1){
      this.setState({
        scrollPositionY : scrollPositionY,
        opacity: 1,
        visibility: visibility,
      })
    }
    while(!visibility && this.state.opacity > 0){
      this.setState({
        scrollPositionY : scrollPositionY,
        opacity: 0,
        visibility: visibility,
      })
    }
    this.setState({
      scrollPositionY: scrollPositionY,
      visibility: visibility,
    })

  }
  hideForm = () =>{
    this.setState({
      display: "none",
      visibility: false
    })
  }

  render(){
    const isScrolling = !!this.state.scrollPositionY
    const visibility = (this.state.visibility) ? "visible" : "hidden"

      {if(!this.state.submitted && this.state.visibility){
          return(
            <div
              className="subscription-container"
              style={{
                opacity:this.state.opacity,
                visibility: visibility,
                display: this.state.display

              }}
            >
            {this.props.canBeClosed &&(

              <div
                className="close-popup">
                <i
                  className="fa fa-close close-popup"
                  onClick={this.hideForm}
                ></i>
              </div>
            )}
              <SubscriptionInput
                containerClassName="subscription-content"
                opacity={this.state.opacity}
                showForm={this.state.visibility}
                canBeClosed="true"
                close={this.hideForm}
                heading="Subscribe!"
                headingClass="subscription-popup-heading"
                subheading="Enter your mailaddress to receive updates about my trips"
                subheadingClass="subscription-popup-subheading"
                formClass="popup-form"
                inputClass="form-control"
                buttonClass="btn btn-dark footer-button"
              />
            </div>
          )
        }else{
          return null
        }}
  }
}
