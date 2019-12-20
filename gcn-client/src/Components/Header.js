import React from 'react';
import { Navbar, NavbarBrand } from 'reactstrap';

const Header = (props) => {
    return (
        <Navbar dark color="primary">
            <div className="container">
              <NavbarBrand href="/">GCN App</NavbarBrand>
            </div>
        </Navbar>
    )
}

export default Header;