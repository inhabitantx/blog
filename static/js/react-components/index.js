import React from 'react'
import ReactDOM from 'react-dom'

import SubscriptionInput from './react-subscription-input/SubscriptionInput'
import SubscriptionPopUp from './react-subscription-popup/SubscriptionPopUp'
import PopUpMenu from './react-pop-up-menu/PopUpMenu'


if(document.getElementById('subscription-popup')){
  ReactDOM.render(<SubscriptionPopUp
                    canBeClosed="true"
                  />,
    document.getElementById('subscription-popup')
  )
}
if(document.getElementById('footer-subscription')){
  ReactDOM.render(
    <SubscriptionInput
        containerClassName="footer-subscription"
        formClass="footer-form"
        inputClass="form-control"
        buttonClass="btn btn-dark footer-button"
    />,
    document.getElementById('footer-subscription')
  )
}


// predefined MenuItems for the PopUp

const MENUITEMS = [
  {
    name : 'Recent',
    link: '/blog',
    url : 'fetcharticles',
    keyword: 'Recent',
  },
  {
    name : 'Travel',
    link: '/blog/travel',
    url : 'fetcharticles',
    keyword: 'Travel',
  },
  {
    name : 'Work',
    link: '/blog/work',
    url : 'fetcharticles',
    keyword: 'Work',
  },
  {
    name : 'Photography',
    link: '/blog/photography',
    url : 'fetcharticles',
    keyword: 'Photography',
  },
]

if(document.getElementById('react-popupmenu')){
  ReactDOM.render(
    <PopUpMenu items={MENUITEMS} />,
    document.getElementById('react-popupmenu')
  );
}
