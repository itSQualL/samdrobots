#include "drobots.ice"

module services {

  exception AlreadyExists { string key; };
  exception NoSuchKey { string key; };

  dictionary<string, Object*> GamePrxsDict;

  interface Container {
    void link(string key, Object* proxy) throws AlreadyExists;
    void unlink(string key) throws NoSuchKey;
    GamePrxsDict list();
  };

  interface ControllerFactory {
     drobots::RobotController* make(drobots::Robot* bot);
     drobots::DetectorController* makeDetectorController();
  };
};
