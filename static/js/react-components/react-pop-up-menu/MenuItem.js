
import React from 'react'
import RenderDom from 'react-dom'

import PopUp from './PopUp'




export default class MenuItem extends React.Component {
  constructor(props){
    super(props)

    this.state = {
      showMenu : false,
    }

  }

  componentWillUnmount(){
    clearTimeout(this.wait)
  }
  handleMouseOver = () => {
    if(this.wait){
      clearTimeout(this.wait)
    }
    this.setState({
      showMenu: true,
      })

  }

  handleMouseOut = () => {
      this.wait = setTimeout(() => {
        this.setState({
          showMenu: false,
      })
    },100)
  }

  render(){

    return(
        <a className="react-menu-item-link" href={this.props.item.link}>
          <div
            className="react-menu-item dropdown-item"
            onMouseEnter={this.handleMouseOver}
            onMouseLeave={this.handleMouseOut}
          >
            <i className="fa fa-plus"></i>
              {this.props.name}
            {this.state.showMenu &&
              <PopUp
                visibility={this.state.showMenu}
                enter={this.handleMouseOver}
                leave={this.handleMouseOut}
                name={this.props.name}
                item={this.props.item}
              />
            }
          </div>
        </a>
    )
  }
}
