import React, {useState} from "react";
import {SortableContainer, SortableElement, SortableHandle} from "react-sortable-hoc";
import arrayMove from "array-move";
import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";
import ListItemIcon from "@material-ui/core/ListItemIcon";
import ListItemText from "@material-ui/core/ListItemText";
import ListItemSecondaryAction from "@material-ui/core/ListItemSecondaryAction";
import DragHandleIcon from "@material-ui/icons/DragHandle";

const DragHandle = SortableHandle(() => (
    <ListItemIcon>
        <DragHandleIcon/>
    </ListItemIcon>
));

const SortableItem = SortableElement(({text}) => (
    <ListItem ContainerComponent="div">
        <ListItemText primary={text}/>
        <ListItemSecondaryAction>
            <DragHandle/>
        </ListItemSecondaryAction>
    </ListItem>
));

const SortableListContainer = SortableContainer(({items}) => (
    <List component="div">
        {items.map(({id, text}, index) => (
            <SortableItem key={id} index={index} text={text}/>
        ))}
    </List>
));

const SortableList = () => {
    const [items, setItems] = useState([
        {id: "1", text: "map 1"},
        {id: "2", text: "map 2"},
        {id: "3", text: "map 3"},
        {id: "4", text: "map 4"}
    ]);

    const onSortEnd = ({oldIndex, newIndex}) => {
        setItems(items => arrayMove(items, oldIndex, newIndex));
    };

    return (
        <SortableListContainer
            items={items}
            onSortEnd={onSortEnd}
            useDragHandle={true}
            lockAxis="y"
        />
    );
};

export default SortableList
