import * as React from 'react';
import { MyFavoriteAnimal } from './MyFavoriteAnimal';
export class MyFavoriteAnimalList
extends React.Component {
 render() {
 const listItems = this.props.animals.map((a) => {
 return <MyFavoriteAnimal key={a} animal={a} />;
 });
 return (
 <div>
 My Favorite Animals:
 <ul>{listItems}</ul>
 </div>
 );
 }
}