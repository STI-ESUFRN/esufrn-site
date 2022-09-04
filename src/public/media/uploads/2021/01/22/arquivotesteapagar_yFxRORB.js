/* eslint-disable react-hooks/exhaustive-deps */
/* eslint-disable react-native/no-inline-styles */
import React, {useState, useEffect} from 'react';
import {
  ActivityIndicator,
  TouchableOpacity,
  View,
  Text,
  TextInput,
} from 'react-native';
import {Container, Content} from 'native-base';
import {
  CodeField,
  Cursor,
  useBlurOnFulfill,
  useClearByFocusCell,
} from 'react-native-confirmation-code-field';
import Header from '~/components/Header';
import CustomAlert from '~/components/CustomAlert';
