import React from 'react'
import RenderDom from 'react-dom'

import MenuItem from './MenuItem'




export default class PopUpMenu extends React.Component {


  render(){

      this.menuitems = this.props.items.map(item => {
        return(
            <MenuItem
                key={item.name}
                name={item.name}
                item={item}
            />
        )
      })

    return (
              <div>
                {this.menuitems}
              </div>
      )
  }
}
