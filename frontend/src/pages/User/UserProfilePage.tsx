import {SelfUserProfilePage} from "./SelfUserProfilePage.tsx";
import {DifferentUserProfilePage} from "./DifferentUserProfilePage.tsx";
import {useParams} from "react-router-dom";
import {getUsernameFromToken} from "../../utils/authentication.ts"

export const UserProfilePage = () => {
    const { username: profileUsername } = useParams();
    const loggedInUsername = getUsernameFromToken();

    if (profileUsername === loggedInUsername) {
        return <SelfUserProfilePage />;
    }

    return <DifferentUserProfilePage username={profileUsername} />;
};