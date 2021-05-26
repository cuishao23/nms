import state from "./state";

const getters = {
    // terminal_list
    getTerminalSelectionList:(state)=>{
        return state.terminal_selection_list
    },
    // terminal_list
    getGrabfileSelectionList:(state)=>{
        return state.grabfile_selection_list
    }
};
export default getters
