import React from 'react';
import FormControl from "@material-ui/core/FormControl";
import InputLabel from "@material-ui/core/InputLabel";
import Select from "@material-ui/core/Select";
import MenuItem from "@material-ui/core/MenuItem";
import IconButton from "@material-ui/core/IconButton";
import DeleteIcon from '@material-ui/icons/Delete';
import CheckIcon from '@material-ui/icons/Check';
import List from "@material-ui/core/List";
import SortableList from "./mapRotationList";
import ListItem from "@material-ui/core/ListItem";
import Grid from "@material-ui/core/Grid";
import TextField from "@material-ui/core/TextField";
import {ListItemSecondaryAction} from "@material-ui/core";
import AddIcon from "@material-ui/icons/Add";

const AddMapRotationPresetItem = ({classes, newPresetName, setNewPresetName, onAdd}) => (
    <ListItem>
        <Grid container>
            <Grid item xs={6} className={classes.paddingRight}>
                <TextField InputLabelProps={{
                    shrink: true,
                }} label="New Preset Name" value={newPresetName} onChange={
                    (e) => setNewPresetName(e.target.value)}/>
            </Grid>
        </Grid>

        <ListItemSecondaryAction>
            <IconButton edge="end" aria-label="delete" onClick={() => onAdd(newPresetName).then(() => {
                setNewPresetName("");
            })}>
                <AddIcon/>
            </IconButton>
        </ListItemSecondaryAction>

    </ListItem>
)

//
// const MapRotationPresetEditableList = ({classes, nameList, onDelete, onAdd, onEdit, onActivate}) => {
//     const [name, setName] = React.useState("")
//
//     return <React.Fragment>
//         <List dense>
//             <AddMapRotationPresetItem classes={classes} name={name} setName={setName} onAdd={onAdd}/>
//             {nameList.map(obj => (
//                 <ListItem key={obj.name}>
//                     <ListItemText
//                         primary={obj}
//                         // primary={obj.name}
//                     />
//                     <ListItemSecondaryAction>
//                         <IconButton edge="end" aria-label="delete" onClick={() => onDelete(obj.name)}>
//                             <DeleteIcon/>
//                         </IconButton>
//                         <IconButton edge="end" aria-label="edit" onClick={() => onEdit(obj.name)}>
//                             <EditIcon/>
//                         </IconButton>
//                         <IconButton edge="end" aria-label="activate" onClick={() => onActivate(obj.name)}>
//                             <CheckIcon/>
//                         </IconButton>
//                     </ListItemSecondaryAction>
//                 </ListItem>
//             ))}
//             <AddMapRotationPresetItem classes={classes} name={name} setName={setName} onAdd={onAdd}/>
//         </List>
//     </React.Fragment>
// };
//
// export default MapRotationPresetEditableList


const MapRotationPresetForm = ({classes, onDelete, onAdd, onActivate,
                                   onChangeEditingPreset}) => {
    const handleSelectFormChange = (event) => {
        setName(event.target.value);
    };

    const [selectedPreset, setName] = React.useState('');
    const [newPresetName, setNewPresetName] = React.useState('');

    return <React.Fragment>
        <List dense>
            <FormControl variant="outlined" classes={classes}>
                <InputLabel>Rotation Preset</InputLabel>
                <Select
                    value={selectedPreset}
                    onChange={handleSelectFormChange}
                    displayEmpty
                    defaultValue={""}
                    inputProps={{'aria-label': 'Without label'}}
                >
                    <MenuItem value={0}>Standard Preset</MenuItem>
                    <MenuItem value={1}>Seeding Preset</MenuItem>
                    <MenuItem value={2}>Friday Fun Preset</MenuItem>
                </Select>

            </FormControl>

            <IconButton edge="end" aria-label="delete" onClick={() => onDelete(selectedPreset)}>
                <DeleteIcon/>
            </IconButton>

            <IconButton edge="end" aria-label="activate" onClick={() => onActivate(selectedPreset)}>
                <CheckIcon/>
            </IconButton>

            <AddMapRotationPresetItem
                classes={classes} newPresetName={newPresetName} setNewPresetName={setNewPresetName}
                onAdd={onAdd}
            />

        </List>

        <p>Editing '{selectedPreset}'</p>

        <SortableList>

        </SortableList>

    </React.Fragment>

};

export default MapRotationPresetForm;
